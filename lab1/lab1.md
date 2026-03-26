---
title: "人工智能实验报告"
subtitle: "中山大学计算机学院本科生实验报告"
author:
  - "课程名称：Artificial Intelligence"
  - "学号：24344064"
  - "姓名：廖海涛"
date: "3/26/2026"
---

# 实验题目

<!-- 在此填写实验题目 -->
- 作业 1
  - 命题逻辑的归结推理
  - 最一般合一算法
- 作业 2
  - 例题 Graduate Student
  - 例题 Alpine Club

# 实验内容

## 算法原理

### 命题逻辑的归结推理

归结推理是基于反证法, 通过不断消去互补的 literals, 最终推出空子句, 从而证明构造的命题不可满足, 即原结论成立.

实现时, 将结论的否定加入 KB, 将子句写为 CNF 的形式, 随后不断使用归结, 从两个子句中消去互补文字, 直到得到空子句或无法得到新子句.

### 最一般合一算法

最一般合一算法是一种用于找到两个表达式之间的最一般替换, 使得它们在某些条件下相等.

算法通过递归地比较两个表达式的结构, 如果遇到变量, 则记录下该变量与另一个表达式的关系. 如果遇到函数或常量, 则检查它们是否相同. 最终返回一个替换列表, 其中包含了所有变量与其对应表达式的关系.


# 关键代码展示

## 命题逻辑的归结推理

此处省略了一些处理细节. 部分细节可见[优化 & 创新](#创新点--优化).

```python {.numberLines}
def resolutionProp(clauses_input: List[str], max_steps: int = 500) -> List[str]:
    # ...
    generated_any = True
    step_guard = 0

    while generated_any and step_guard < max_steps:
        generated_any = False
        step_guard += 1
        n = len(clauses)
        for i in range(n):
            for j in range(i):
                # ...
                for p, l1 in enumerate(c1):
                    for q, l2 in enumerate(c2):
                        s = unify_literals(l1, l2)
                        # (MGU) 尝试合一两个 Literal
                        # ...
                        rem1 = [x for k, x in enumerate(c1) if k != p]
                        rem2 = [x for k, x in enumerate(c2) if k != q]
                        resolvent = apply_subst_clause(tuple(rem1 + rem2), s)
                        # ...
                        if len(resolvent) == 0:   # 得到空子句, 证明成功
                            for line in steps:
                                print(line)
                            return steps
    # ...
```

## 最一般合一算法

```python {.numberLines}
def unify_literals(l1: Literal, l2: Literal) -> Optional[Subst]:
    if not l1.complementary_to(l2):     # 先判断是否可能互补, 否则没必要合一
        return None
    s: Subst = {}
    for a, b in zip(l1.args, l2.args):
        s = unify_term(a, b, s)         # 递归尝试合一每一项
        if s is None:
            return None
    return s

def unify_term(t1: Term, t2: Term, s: Subst) -> Optional[Subst]:
    # ...
    if t1 == t2:
        return s
    if t1.is_var():
        return unify_var(t1, t2, s)     # 变量合一
    if t2.is_var():
        return unify_var(t2, t1, s)
    if t1.name != t2.name or len(t1.args) != len(t2.args):
        return None
    for a, b in zip(t1.args, t2.args):
        s = unify_term(a, b, s)         # 递归合一函数参数
        if s is None:
            return None
    return s

def unify_var(v: Term, t: Term, s: Subst) -> Optional[Subst]:
    if v.name in s:
        return unify_term(s[v.name], t, s)
    if t.is_var() and t.name in s:
        return unify_term(v, s[t.name], s)
    if occurs(v.name, t, s):            # 检查 v 是否出现在 t 中, 防止无限递归替换
        return None
    s[v.name] = t
    return s
```

# 创新点 & 优化

<!-- 描述你的创新点或优化方法 -->
直觉上来看, 短的子句更容易得到空子句, 因此在归结过程中优先处理短子句可能更快地得到结果. 具体实现时, 在每次生成新子句后, 对所有子句按照长度进行排序, 优先处理较短的子句. 实际上, 对于较长的归结过程减少了 30%\~40% 的步骤. 虽然有排序开销, 但是算法的时间瓶颈在指数级的 MGU 算法.

# 实验结果及分析

## 实验结果展示示例

对于所有幻灯片中的例题, 结果均正确. 以 Alpine Club 作业 2 为例, 输出如下:

```
1. (On(tony,mike))
2. (On(mike,john))
3. (Green(tony))
4. (~Green(john))
5. (Green(yy),~Green(xx),~On(xx,yy))
6. R[1a,5c]{var_5_xx=tony,var_5_yy=mike} (Green(mike),~Green(tony))
7. R[2a,5c]{var_5_xx=mike,var_5_yy=john} (Green(john),~Green(mike))
8. R[3a,5b]{var_5_xx=tony} (Green(v5_yy),~On(tony,v5_yy))
9. R[4a,5a]{var_5_yy=john} (~Green(v5_xx),~On(v5_xx,john))
10. R[3a,6b]{} (Green(mike))
11. R[4a,7a]{} (~Green(mike))
12. R[6a,7b]{} (Green(john),~Green(tony))
13. R[6a,5b]{var_5_xx=mike} (Green(v5_yy),~Green(tony),~On(mike,v5_yy))
14. R[6b,5a]{var_5_yy=tony} (Green(mike),~Green(v5_xx),~On(v5_xx,tony))
15. R[7a,5b]{var_5_xx=john} (Green(v5_yy),~Green(mike),~On(john,v5_yy))
16. R[7b,5a]{var_5_yy=mike} (Green(john),~Green(v5_xx),~On(v5_xx,mike))
17. R[8a,5b]{var_5_xx=v5_yy} (Green(v5_yy),~On(tony,v5_yy),~On(v5_yy,v5_yy))
18. R[9a,5a]{var_5_yy=v5_xx} (~Green(v5_xx),~On(v5_xx,john),~On(v5_xx,v5_xx))
19. R[3a,12b]{} (Green(john))
20. R[3a,13b]{} (Green(v5_yy),~On(mike,v5_yy))
21. R[4a,12a]{} (~Green(tony))
22. R[4a,16a]{} (~Green(v5_xx),~On(v5_xx,mike))
23. R[10a,11a]{} ()
```

其他结果可以见 [output.txt](./output.txt).

## 评测指标展示及分析

解决 7 道例题总用时 273ms(包含 I/O).

其中单独解决每道题目的用时如下:

| 例题 | 用时 (ms) |
| --- | --- |
| Graduate Student 例题 | 86 |
| Alpine Club 作业 1 | 257 |
| Alpine Club 作业 2 | 74 |

<!-- 在此分析评测指标 -->

---

# 参考资料

包含 AIGC. 使用了 GitHub Copilot.
