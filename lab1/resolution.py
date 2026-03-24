from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Set, Tuple


@dataclass(frozen=True)
class Term:
    """
    字段类型：
    - name: str
      项名。无参时可表示变量或常量；有参时表示函数符号名。
    - args: tuple[Term, ...]
      参数项列表。空元组表示原子项（变量/常量），非空表示函数项。

    - Term("x") -> 变量 x（按 is_var 规则判断）
    - Term("a") -> 常量 a
    - Term("g", (Term("x"),)) -> 函数项 g(x)
    """
    name: str
    args: Tuple["Term", ...] = ()

    def is_var(self) -> bool:
        # 规则：无参项且名字仅包含 x/y/z/u/v/w 字符，则视作变量；内部标准化变量 var_* 也视作变量。
        if len(self.args) != 0:
            return False
        if self.name.startswith("var_"):
            return True
        return bool(self.name) and all(ch in {"x", "y", "z", "u", "v", "w"} for ch in self.name)

    def __str__(self) -> str:
        if not self.args:
            return self.name
        return f"{self.name}({','.join(str(a) for a in self.args)})"


@dataclass(frozen=True)
class Literal:
    """
    一阶逻辑 Literal。

    字段类型：
    - neg: bool
      True 表示 ~P(...)；False 表示 P(...)。
    - pred: str
      谓词名（例如 P、Student）。
    - args: tuple[Term, ...]
      谓词参数项。
    """
    neg: bool
    pred: str
    args: Tuple[Term, ...]

    def complementary_to(self, other: "Literal") -> bool:
        """
        判断两个文字是否可能互补(如 P(x) 和 ~P(x))：
        - 谓词名相同
        - 否定号相反
        - 参数个数一致

        NOTE 只判断形状(具体内容在合一的时候做)
        """
        return self.pred == other.pred and self.neg != other.neg and len(self.args) == len(other.args)

    def __str__(self) -> str:
        head = f"{self.pred}"
        if self.args:
            head += f"({','.join(str(a) for a in self.args)})"
        return f"~{head}" if self.neg else head


Clause = Tuple[Literal, ...]
Subst = Dict[str, Term]
# 类型别名说明：
# - Clause: tuple[Literal, ...]，一个子句（Literal 析取）(保证一定 Normalized)
# - Subst: dict[str, Term]，替换（变量名 -> 项）


# ---------- parsing ----------
def split_top_level(s: str, sep: str = ",") -> List[str]:
    """
    按顶层分隔符切分字符串，不切开括号内部内容。

    参数：
    - s: str
      原始字符串，如 "P(x),Q(g(x)),R(a,b)"。
    - sep: str = ","
      分隔符字符。默认为半角逗号","

    返回：
    - list[str]
      切分后的片段列表（已 strip）。
    """
    parts: List[str] = []
    level = 0
    start = 0
    for i, ch in enumerate(s):
        if ch == "(":
            level += 1
        elif ch == ")":
            level -= 1
        elif ch == sep and level == 0:
            parts.append(s[start:i].strip())
            start = i + 1
    tail = s[start:].strip()
    if tail:
        parts.append(tail)
    return parts


def parse_term(text: str) -> Term:
    """
    将字符串解析为 Term。
    """
    text = text.strip()
    if "(" not in text:
        return Term(text)
    i = text.find("(")
    name = text[:i].strip()
    inside = text[i + 1 : -1].strip()
    args = tuple(parse_term(x) for x in split_top_level(inside, ","))
    return Term(name, args)


def parse_literal(text: str) -> Literal:
    """
    将字符串解析为 Literal。
    """
    text = text.strip()
    neg = text.startswith("~")
    if neg:
        text = text[1:].strip()
    if "(" not in text:
        return Literal(neg, text, ())
    i = text.find("(")
    pred = text[:i].strip()
    inside = text[i + 1 : -1].strip()
    args = tuple(parse_term(x) for x in split_top_level(inside, ","))
    return Literal(neg, pred, args)


def parse_clause(text: str) -> Clause:
    """
    将字符串解析为 Clause。
    """
    text = text.strip()
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1].strip()
    if not text:
        return tuple()
    lits = tuple(parse_literal(x) for x in split_top_level(text, ","))
    return normalize_clause(lits)


# ---------- substitution / unification ----------
def apply_subst_term(t: Term, s: Subst) -> Term:
    """
    对单个 Term 应用替换。
    """
    if t.is_var() and t.name in s:
        return apply_subst_term(s[t.name], s)
    if not t.args:
        return t
    return Term(t.name, tuple(apply_subst_term(a, s) for a in t.args))


def apply_subst_lit(l: Literal, s: Subst) -> Literal:
    """
    对单个 Literal 应用替换。
    """
    return Literal(l.neg, l.pred, tuple(apply_subst_term(a, s) for a in l.args))


def apply_subst_clause(c: Clause, s: Subst) -> Clause:
    """
    对整个 Clause 应用替换，并做归一化（去重+排序）。
    """
    return normalize_clause(tuple(apply_subst_lit(l, s) for l in c))


def occurs(var_name: str, t: Term, s: Subst) -> bool:
    """
    occurs-check：变量 var_name 是否出现在项 t 中（做完替换 s 之后）。
    """
    t = apply_subst_term(t, s)
    if t.is_var():
        return t.name == var_name
    return any(occurs(var_name, a, s) for a in t.args)


def unify_var(v: Term, t: Term, s: Subst) -> Optional[Subst]:
    """
    合一中的“变量-项”分支处理。

    paras:
    - v: Term
      必须是变量项。
    - t: Term
      任意项。
    - s: Subst
      当前替换（会原地扩展）。

    returns:
    - Optional[Subst]
      成功返回替换字典；失败返回 None。
    """
    if v.name in s:
        return unify_term(s[v.name], t, s)
    if t.is_var() and t.name in s:
        return unify_term(v, s[t.name], s)
    if occurs(v.name, t, s):
        return None
    s[v.name] = t
    return s


def unify_term(t1: Term, t2: Term, s: Subst) -> Optional[Subst]:
    """
    合一两个项（递归）。

    参数：
    - t1: Term
    - t2: Term
    - s: Subst
      当前替换（会原地扩展）。

    返回：
    - Optional[Subst]
      成功返回扩展后的替换；失败返回 None。
    """
    t1 = apply_subst_term(t1, s)
    t2 = apply_subst_term(t2, s)
    if t1 == t2:
        return s
    if t1.is_var():
        return unify_var(t1, t2, s)
    if t2.is_var():
        return unify_var(t2, t1, s)
    if t1.name != t2.name or len(t1.args) != len(t2.args):
        return None
    for a, b in zip(t1.args, t2.args):
        s = unify_term(a, b, s)
        if s is None:
            return None
    return s


def unify_literals(l1: Literal, l2: Literal) -> Optional[Subst]:
    """
    合一两个互补文字的参数。

    参数：
    - l1: Literal
    - l2: Literal

    返回：
    - Optional[Subst]
      若文字不互补或合一失败则 None；成功返回 MGU。
    """
    if not l1.complementary_to(l2):
        return None
    s: Subst = {}
    for a, b in zip(l1.args, l2.args):
        s = unify_term(a, b, s)
        if s is None:
            return None
    return s


# ---------- resolution ----------
def normalize_clause(c: Sequence[Literal]) -> Clause:
    """
    子句归一化：去重并按字符串排序，便于判重。
    """
    uniq = sorted(set(c), key=str)
    return tuple(uniq)


def alpha(i: int) -> str:
    """
    将文字下标转字母标签。用于 R[1a]
    """
    return chr(ord("a") + i)


def subst_str(s: Subst) -> str:
    """
    将替换字典 格式化为 输出字符串。
    """
    if not s:
        return "{}"
    items = sorted((k, str(apply_subst_term(v, s))) for k, v in s.items())
    return "{" + ",".join(f"{k}={v}" for k, v in items) + "}"


def clause_str(c: Clause) -> str:
    """
    将 Clause 格式化为 "(...,...)"。
    """
    return "(" + ",".join(str(l) for l in c) + ")"


def standardize_apart(clause: Clause, idx: int) -> Clause:
    """
    对子句做变量标准化（standardize apart），避免不同子句变量名冲突。

    参数：
    - idx: int
      子句编号，用于生成唯一变量前缀（var_{idx}_...）。

    返回：
    - Clause
      标准化后的子句。

    主要是为了避免不同子句使用同一个变量名可能产生的冲突：x -> var_idx_x
    """
    rename: Dict[str, Term] = {}

    def map_term(t: Term) -> Term:
        if t.is_var():
            if t.name not in rename:
                rename[t.name] = Term(f"var_{idx}_{t.name}")
            return rename[t.name]
        if not t.args:
            return t
        return Term(t.name, tuple(map_term(a) for a in t.args))

    return normalize_clause(
        tuple(Literal(l.neg, l.pred, tuple(map_term(a) for a in l.args)) for l in clause)
    )


def resolutionProp(clauses_input: List[str], max_steps: int = 500) -> List[str]:
    """
    归结推理：输入 list[str]，每个元素是一个子句字符串。
    返回并打印每一步（初始子句 + 归结步骤）。

    参数：
    - clauses_input: list[str]
      子句集输入。每个元素可写成 "(P(x),Q(g(x)))" 或 "P(x),Q(g(x))"。
      约定：否定用 "~"（如 "~P(a)"）。
    - max_steps: int = 500
      最大外层迭代轮数. 防止无限生成

    返回：
    - list[str]
      推理步骤文本列表。格式示例：
      "1. (P(x),Q(g(x)))"
      "3. R[1a,2c]{x=a} (Q(g(a)),R(a),Q(z))"

    关键局部变量：
    - clauses: list[Clause]
      当前已知子句（含初始与新归结子句）。
    - clause_to_id: dict[Clause, int]
      子句到编号的映射，用于判重和输出编号。
    - steps: list[str]
      所有输出行。
    - c1, c2: Clause
      当前参与归结的两个 Cluase。
    - p, q: int
      在 c1/c2 中被选中的 Literal 下标（用于 1a/2c 输出）。
    - s: Optional[Subst]
      当前候选 Literal Pair 的合一结果；None 表示不可合一。
    - resolvent / pretty_res: Clause
      新归结子句（内部版/展示版）。
    """
    clauses: List[Clause] = []
    clause_to_id: Dict[Clause, int] = {}
    steps: List[str] = []

    # 初始子句
    for raw in clauses_input:
        c = parse_clause(raw)
        if c in clause_to_id:
            continue
        clause_id = len(clauses) + 1
        clauses.append(c)
        clause_to_id[c] = clause_id
        steps.append(f"{clause_id}. {clause_str(c)}")

    generated_any = True
    step_guard = 0

    while generated_any and step_guard < max_steps:
        generated_any = False
        step_guard += 1
        n = len(clauses)
        for i in range(n):
            for j in range(i + 1, n):
                c1 = standardize_apart(clauses[i], i + 1)
                c2 = standardize_apart(clauses[j], j + 1)
                for p, l1 in enumerate(c1):
                    for q, l2 in enumerate(c2):
                        s = unify_literals(l1, l2)
                        if s is None:
                            continue
                        rem1 = [x for k, x in enumerate(c1) if k != p]
                        rem2 = [x for k, x in enumerate(c2) if k != q]
                        resolvent = apply_subst_clause(tuple(rem1 + rem2), s)

                        # 将标准化变量名还原为通用 x/y/z 风格前缀变量展示, 为了输出可读
                        pretty_res = tuple(
                            Literal(
                                lit.neg,
                                lit.pred,
                                tuple(
                                    Term(a.name.replace("var_", "v"), a.args)
                                    if (a.is_var() and a.name.startswith("var_"))
                                    else a
                                    for a in lit.args
                                ),
                            )
                            for lit in resolvent
                        )
                        pretty_res = normalize_clause(pretty_res)

                        if pretty_res in clause_to_id:
                            continue

                        new_id = len(clauses) + 1
                        clauses.append(pretty_res)
                        clause_to_id[pretty_res] = new_id
                        generated_any = True

                        src1 = f"{i+1}{alpha(p)}"
                        src2 = f"{j+1}{alpha(q)}"
                        steps.append(
                            f"{new_id}. R[{src1},{src2}]{subst_str(s)} {clause_str(pretty_res)}"
                        )

                        if len(pretty_res) == 0:
                            for line in steps:
                                print(line)
                            return steps

    for line in steps:
        print(line)
    return steps


if __name__ == "__main__":
    print("=== Problem 1 ===")
    kb1 = [
        "(P(x),Q(g(x)))",
        "(R(a),Q(z),~P(a))",
        "(~Q(g(a)))",
        "(~R(a))",
    ]
    resolutionProp(kb1)

    print("\n=== Problem 2 ===")
    kb2 = [
        "(Student(tony))",
        "(~Student(x),Smart(x))",
        "(~Smart(tony))",
    ]
    resolutionProp(kb2)

    print("\n=== Problem 3 ===")
    kb3 = [
        "(A(x),B(x))",
        "(~A(a))",
        "(~B(a))",
    ]
    resolutionProp(kb3)
    
    print("\n=== Problem 4 ===")
    kb4 = [
        "(FirstGrade)",
        "(~FirstGrade,Child)",
        "(~Child)",
    ]
    resolutionProp(kb4)


    print("\n=== Problem 5 ===")
    kb5 = [
        "GradStudent(sue)",
        "(~GradStudent(x), Student(x))",
        "(~Student(x), HardWorker(x))",
        "~HardWorker(sue)"
    ]
    resolutionProp(kb5)

    print("\n=== Problem 6 ===")
    kb6 = [
        "A(tony)",
        "A(mike)",
        "A(john)",
        "L(tony, rain)",
        "(~A(x), S(x), C(x))",
        "(~C(y), ~L(y, rain))",
        "(L(z, snow), ~S(z))",
        "(~L(tony, u), ~L(mike, u))",
        "~(L(tony, v), L(mike, v))",
        "(~A(w), ~C(w), S(w))"
    ]
    resolutionProp(kb6)

    print("\n=== Problem 7 ===")
    kb7 = [
        "On(tony, mike)",
        "On(mike, john)",
        "Green(tony)",
        "~Green(john)",
        "(~On(xx, yy), ~Green(xx), Green(yy))"
    ]
    resolutionProp(kb7)
