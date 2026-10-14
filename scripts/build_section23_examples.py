"""Author the bilingual concepts and textbook examples; coverage is read separately."""
import json
import fitz
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content'
ASSETS = CONTENT / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)
COURSE = {'id': 'stewart-calculus-7e', 'title': 'Stewart 微积分', 'en': {'title': 'Stewart Calculus'}}

def steps(rows):
    return ([{'title': zt, 'body': zb} for zt, zb, et, eb in rows],
            [{'title': et, 'body': eb} for zt, zb, et, eb in rows])

def concept(cid, title, etitle, summary, esummary, rows, pitfalls, ep):
    z, e = steps(rows)
    return dict(id=cid, title=title, summary=summary, method=z, pitfalls=pitfalls,
                en=dict(title=etitle, summary=esummary, method=e, pitfalls=ep))

concepts = [
    concept('limit-laws', '极限定律与图像读值', 'Limit laws and reading graphs',
        r'若 $\lim_{x\to a}f(x)=L$、$\lim_{x\to a}g(x)=M$ 都存在，则和、差、常数倍、积分别趋于 $L+M,L-M,cL,LM$；商趋于 $L/M$ 要求 $M\ne0$。正整数次幂趋于 $L^n$。常数的极限等于常数，$\lim_{x\to a}x=a$。',
        r'If $\lim_{x\to a}f(x)=L$ and $\lim_{x\to a}g(x)=M$ exist, the limits of their sum, difference, constant multiple, and product are $L+M,L-M,cL,LM$. The quotient tends to $L/M$ only when $M\ne0$. A positive integer power tends to $L^n$. A constant tends to itself, and $\lim_{x\to a}x=a$.',
        [
            ('先检查每个极限', '从左右两侧读取曲线趋近的高度，区分实心点的函数值与曲线的极限。', 'Check the component limits', 'Read the approached height from both sides. Distinguish a filled point, which gives the function value, from the limit of the curve.'),
            ('检查法则的条件', r'只有各极限存在才直接组合；除法还需分母极限非零。若一个双侧极限不存在，改算左右两侧。', 'Check the hypotheses', r'Combine existing limits; division also requires a nonzero denominator limit. If a two-sided component limit fails, calculate the two one-sided limits instead.'),
            ('代入极限值并计算', r'写出所用法则和具体运算。左右结果相同时才给出双侧极限。', 'Substitute the limiting values', r'Show the law and the arithmetic. A two-sided limit exists only when the two one-sided results agree.')
        ],
        [r'分母趋于 $0$ 不能直接用商法则。', r'不能把不存在的极限当作数字相加或相乘。'],
        [r'Do not apply the Quotient Law when the denominator tends to $0$.', r'An absent limit cannot be treated as a number in a sum or product.']),
    concept('substitution', '直接代入与根式条件', 'Direct substitution and root conditions',
        r'多项式在每个实数处都可直接代入；有理函数在原分母非零处可直接代入。根式法则为 $\lim\sqrt[n]{f(x)}=\sqrt[n]{L}$，其中 $n$ 是正整数；本节对偶数 $n$ 的法则要求 $L>0$，边界 $L=0$ 要结合定义域或夹逼证明。',
        r'Use direct substitution for a polynomial at every real number and for a rational function wherever its original denominator is nonzero. The Root Law gives $\lim\sqrt[n]{f(x)}=\sqrt[n]{L}$ for a positive integer $n$. The law stated in this section assumes $L>0$ for even $n$; at the boundary $L=0$, check the domain or use a squeeze argument.',
        [
            ('检查定义域', r'确认分母在趋近点不为 $0$，根式在所考虑的邻域内有定义。', 'Check the domain', r'Confirm that the denominator is nonzero at the approach point and radicals are defined on the relevant neighborhood.'),
            ('按法则逐层代入', r'先算幂与多项式，再算积、商、根或外层幂。', 'Apply the laws in order', r'Evaluate powers and polynomials first, then the product, quotient, root, or outer power.'),
            ('计算并解释', r'写出精确结果；应用题还要检查单位及允许的趋近方向。', 'Calculate and interpret', r'Give the exact result. For applications, also check units and the allowed direction of approach.')
        ],
        [r'$0/0$ 是需要变形的信号，不是答案。', r'直接代入性质不适用于原分母为零的点。'],
        [r'$0/0$ signals a need for simplification; it is not an answer.', r'Direct substitution is unavailable where the original denominator is zero.']),
    concept('cancellation', '因式分解、约分与去心邻域', 'Factoring, cancellation, and punctured neighborhoods',
        r'极限只研究 $x$ 接近 $a$ 且 $x\ne a$ 时的行为。若两个函数在这样的邻域中相等，它们在 $a$ 的极限相同。遇到 $0/0$，可先分解并约去共同因子，再求简化后函数的极限。',
        r'A limit concerns $x$ near $a$ with $x\ne a$. Functions equal on such a punctured neighborhood have the same limit at $a$. For a $0/0$ form, factor and cancel a common factor before evaluating the simpler limit.',
        [
            ('试代入，辨认未定式', r'若分子、分母同时趋于 $0$，寻找平方差、立方和差或一般多项式因式。', 'Identify the indeterminate form', r'If both numerator and denominator tend to $0$, look for a difference of squares, a sum or difference of cubes, or polynomial factors.'),
            ('注明条件后约分', r'只在被约因子非零时写出等式；保留原函数的排除点。', 'Cancel with the restriction stated', r'Write the equality only where the canceled factor is nonzero. Retain the excluded points of the original function.'),
            ('求简式极限', r'检查简式的分母，再代入。单个点处无定义或被重新赋值不会改变极限。', 'Evaluate the simpler limit', r'Check the remaining denominator and substitute. An undefined or reassigned value at a single point does not change the limit.')
        ],
        [r'约分不会使原函数在被排除点自动有定义。', r'分子趋非零、分母趋零时，应检查符号与两侧行为，而非硬套约分。'],
        [r'Cancellation does not define the original function at an excluded point.', r'If the numerator tends to a nonzero number while the denominator tends to zero, examine signs and one-sided behavior.']),
    concept('difference-quotients', '增量形式与差商', 'Increment forms and difference quotients',
        r'本节先用代数处理 $\lim_{h\to0}[F(x+h)-F(x)]/h$，不需要预先使用导数。展开、通分或有理化后，分子通常含 $h$，在 $h\ne0$ 时可约去。',
        r'This section treats $\lim_{h\to0}[F(x+h)-F(x)]/h$ algebraically, without using derivatives. Expansion, a common denominator, or rationalization often reveals a factor of $h$, which can be canceled when $h\ne0$.',
        [
            ('保留原差商', r'注意 $(x+h)^n$ 与 $x^n+h^n$ 不同，参数 $x$ 在 $h\to0$ 时固定。', 'Keep the original quotient', r'$(x+h)^n$ differs from $x^n+h^n$. A parameter $x$ remains fixed while $h\to0$.'),
            ('展开或通分', r'先消去相同常数项，把剩余分子写成 $h$ 乘一个表达式。', 'Expand or combine fractions', r'Cancel the matching constant terms and express the remaining numerator as $h$ times another expression.'),
            ('约去增量，再代入', r'对 $h\ne0$ 约分，检查固定参数的定义域，然后令 $h\to0$。', 'Cancel the increment and substitute', r'Cancel for $h\ne0$, check the domain restrictions on fixed parameters, and then let $h\to0$.')
        ],
        [r'不能先令 $h=0$ 后把 $0/0$ 当作值。', r'参数出现在分母时，必须保留其非零条件。'],
        [r'Do not set $h=0$ and treat $0/0$ as a value.', r'Retain nonzero restrictions on parameters appearing in denominators.']),
    concept('rationalization', '根式差与共轭有理化', 'Radical differences and conjugates',
        r'利用 $(A-B)(A+B)=A^2-B^2$，把根式差变为多项式差。只有乘上同一个非零因子的分子与分母，才能保持原式。',
        r'Use $(A-B)(A+B)=A^2-B^2$ to turn a difference of radicals into a polynomial difference. Multiply numerator and denominator by the same nonzero conjugate.',
        [
            ('找出导致 $0/0$ 的根式差', r'确定根号覆盖范围和原式定义域，选择对应的共轭。', 'Locate the radical difference', r'Check the full radicand and the original domain, then choose the corresponding conjugate.'),
            ('乘共轭并化简', r'写出平方差，约去共同因子；若分子分母都有根式差，可能要先后处理两次。', 'Multiply by the conjugate and simplify', r'Use the difference of squares and cancel common factors. Two radical differences may require rationalizing both in turn.'),
            ('检查简式并求极限', r'确认简化后的分母极限非零，再代入，保留精确根式。', 'Check and evaluate', r'Confirm a nonzero limiting denominator, substitute, and retain exact radical values.')
        ],
        [r'不要把 $\sqrt{x+y}$ 拆成 $\sqrt{x}+\sqrt{y}$。', r'共轭乘法中的平方差必须覆盖整个根式。'],
        [r'Do not split $\sqrt{x+y}$ into $\sqrt{x}+\sqrt{y}$.', r'The difference of squares must use the entire radicand.']),
    concept('one-sided', '单侧极限、绝对值与分段函数', 'One-sided limits, absolute values, and piecewise functions',
        r'$\lim_{x\to a}f(x)=L$ 当且仅当左右极限都等于 $L$。分别使用各侧适用的分支；$|u|=u$ 当 $u\ge0$，$|u|=-u$ 当 $u<0$。',
        r'$\lim_{x\to a}f(x)=L$ if and only if both one-sided limits equal $L$. Use the branch valid on each side; $|u|=u$ for $u\ge0$ and $|u|=-u$ for $u<0$.',
        [
            ('定位分界点与符号', r'列出绝对值内部或分段条件在趋近点两侧的符号。', 'Locate the boundary and signs', r'Determine the signs inside absolute values or the applicable piecewise branch on each side.'),
            ('左右分别计算', r'在每一侧改写原式，独立算出左极限和右极限。', 'Compute each side separately', r'Rewrite the original expression using the valid branch and calculate the left- and right-hand limits independently.'),
            ('比较并检查点值', r'左右相同则双侧极限存在；不同则不存在。需要求函数值时另按该点定义计算。', 'Compare and check point values', r'Equal one-sided values give a two-sided limit; unequal values do not. Calculate the function value separately when requested.')
        ],
        [r'函数值、左极限、右极限是三个不同量。', r'单侧根式极限必须从定义域允许的一侧趋近。'],
        [r'The function value and the two one-sided limits are distinct quantities.', r'Approach a radical boundary from a side allowed by its domain.']),
    concept('floor', '取整函数与跳跃', 'The greatest integer function and jumps',
        r'$[x]=\lfloor x\rfloor$ 是不大于 $x$ 的最大整数。非整数 $a$ 附近取整值保持不变；在整数 $n$ 处左极限为 $n-1$、右极限为 $n$，因此双侧极限不存在。',
        r'$[x]=\lfloor x\rfloor$ is the greatest integer less than or equal to $x$. Near a noninteger $a$, the floor value is constant. At an integer $n$, its left-hand limit is $n-1$ and its right-hand limit is $n$, so the two-sided limit does not exist.',
        [
            ('确定落在哪个整数区间', r'先算输入在趋近点左侧与右侧分别落在哪个 $[n,n+1)$ 内。', 'Identify the integer interval', r'Find the intervals $[n,n+1)$ containing the input on each side of the approach point.'),
            ('分别取整', r'负数向下取整，例如 $[-1/2]=-1$。复合函数要先分析内层值是否跨过整数。', 'Take the floor on each side', r'Round down for negative inputs, for example $[-1/2]=-1$. For a composition, check whether the inner value crosses an integer.'),
            ('比较两侧与函数值', r'先比较两侧常数决定极限，再单独计算点值。图像左端实心、右端空心。', 'Compare sides and the function value', r'Compare the side constants to determine the limit; then calculate the point value separately. Each floor step has a closed left endpoint and an open right endpoint.')
        ],
        [r'取整不是向零截断。', r'取整函数的组合在整数点也可能消除跳跃，应看整个表达式。'],
        [r'The floor function is not truncation toward zero.', r'A combination of floor functions may cancel jumps; examine the entire expression.']),
    concept('squeeze', '夹逼定理、振荡与大小比较', 'Squeeze Theorem, oscillation, and comparison',
        r'若 $F(x)\le G(x)\le H(x)$ 在 $a$ 的去心邻域成立，且两端都趋于同一个 $L$，则中间也趋于 $L$。特别地，$|G(x)|\le B(x)$ 且 $B(x)\to0$ 时有 $G(x)\to0$。',
        r'If $F(x)\le G(x)\le H(x)$ on a punctured neighborhood of $a$ and both bounding functions tend to the same $L$, then $G(x)\to L$. In particular, $|G(x)|\le B(x)$ with $B(x)\to0$ implies $G(x)\to0$.',
        [
            ('建立真实上、下界', r'常用 $-1\le\sin u,\cos u\le1$；乘非负振幅保持不等号，乘负数要反向。', 'Establish valid bounds', r'Use $-1\le\sin u,\cos u\le1$. Multiplying by a nonnegative amplitude preserves the inequality; multiplying by a negative number reverses it.'),
            ('求两端极限', r'确认上下界趋于同一个数；必要时先限定在趋近点附近以保证根式有定义。', 'Evaluate the bounding limits', r'Confirm that both bounds approach the same number. Restrict to a neighborhood when needed to ensure radicals are defined.'),
            ('应用夹逼并解释', r'中间函数可以振荡，但幅度被压至零。图与数值表只辅助观察，证明依靠不等式。', 'Apply the theorem and interpret', r'The middle function may oscillate while its amplitude shrinks to zero. Graphs and tables aid intuition; the inequality supplies the proof.')
        ],
        [r'不能把不存在的 $\lim\sin(1/x)$ 与 $0$ 相乘。', r'两端极限不同，不能由夹逼定理给出中间的唯一极限。'],
        [r'Do not multiply the nonexistent $\lim\sin(1/x)$ by $0$.', r'Bounds with different limits do not force a unique limit.'])
]

examples = []
def example(n, cid, pp, zp, ep, rows, za, ea, **extra):
    z, e = steps(rows)
    q = dict(id=f'example-{n}', type='example', label=f'教材例题 {n}', prompt=zp,
             concept=cid, printedPage=pp, pdfPage=pp+32, steps=z, answer=za,
             en=dict(label=f'Textbook Example {n}', prompt=ep, steps=e, answer=ea), **extra)
    examples.append(q)
    return q

example(1,'limit-laws',99,
    r'利用图 1 中 $f$、$g$ 的图像和极限定律，求下列极限（若存在）：(a) $\lim_{x\to-2}[f(x)+5g(x)]$；(b) $\lim_{x\to1}[f(x)g(x)]$；(c) $\lim_{x\to2}f(x)/g(x)$。',
    r'Use the Limit Laws and the graphs of $f$ and $g$ in Figure 1 to evaluate the following limits, if they exist: (a) $\lim_{x\to-2}[f(x)+5g(x)]$; (b) $\lim_{x\to1}[f(x)g(x)]$; (c) $\lim_{x\to2}f(x)/g(x)$.',
    [
        ('(a) 读图并应用和与常数倍法则', r'在 $x=-2$ 处曲线趋于 $\lim f(x)=1$、$\lim g(x)=-1$。因此 $\lim[f(x)+5g(x)]=1+5(-1)=-4$。$f(-2)$ 的实心点不改变这里的极限。', '(a) Read and combine the limits', r'At $x=-2$, the curves give $\lim f(x)=1$ and $\lim g(x)=-1$. The Sum and Constant Multiple Laws give $1+5(-1)=-4$. The filled point defining $f(-2)$ does not change this limit.'),
        ('(b) 分别求左右乘积极限', r'$\lim_{x\to1}f(x)=2$，但 $g$ 的左极限为 $-2$、右极限为 $-1$。左右乘积分别为 $2(-2)=-4$、$2(-1)=-2$，不相等，故双侧乘积极限不存在。', '(b) Calculate the one-sided product limits', r'$\lim_{x\to1}f(x)=2$, but the left and right limits of $g$ are $-2$ and $-1$. The product limits are $2(-2)=-4$ and $2(-1)=-2$, respectively. Their disagreement proves that the two-sided product limit does not exist.'),
        ('(c) 检查分母与符号', r'$\lim_{x\to2}f(x)\approx1.4>0$、$\lim_{x\to2}g(x)=0$。图中 $g$ 在 2 左侧为负、右侧为正，所以商分别趋于 $-\infty$、$+\infty$；商法则不适用，也无双侧极限。', '(c) Check the denominator and its sign', r'$\lim_{x\to2}f(x)\approx1.4>0$ and $\lim_{x\to2}g(x)=0$. The graph shows $g<0$ to the left of 2 and $g>0$ to the right. The quotient therefore tends to $-\infty$ and $+\infty$ on the two sides; the Quotient Law is unavailable and the two-sided limit does not exist.')
    ],
    r'(a) $-4$；(b) 不存在；(c) 不存在（左侧 $-\infty$，右侧 $+\infty$）。',
    r'(a) $-4$; (b) does not exist; (c) does not exist (left $-\infty$, right $+\infty$).',
    subpartIds=['a','b','c'],sourceImage='assets/example-1.png')

example(2,'substitution',101,
    r'求极限并说明每一步：(a) $\lim_{x\to5}(2x^2-3x+4)$；(b) $\lim_{x\to-2}(x^3+2x^2-1)/(5-3x)$。',
    r'Evaluate the following limits and justify each step: (a) $\lim_{x\to5}(2x^2-3x+4)$; (b) $\lim_{x\to-2}(x^3+2x^2-1)/(5-3x)$.',
    [
        ('(a) 分拆多项式极限', r'和、差、常数倍法则给出 $2\lim x^2-3\lim x+\lim4$。幂法则与基本极限给出 $2(5^2)-3(5)+4=50-15+4=39$。', '(a) Separate the polynomial terms', r'The Sum, Difference, and Constant Multiple Laws give $2\lim x^2-3\lim x+\lim4$. The Power Law and basic limits yield $2(5^2)-3(5)+4=50-15+4=39$.'),
        ('(b) 分别计算分子和分母', r'分子极限为 $(-2)^3+2(-2)^2-1=-8+8-1=-1$。分母极限为 $5-3(-2)=11\ne0$。', '(b) Evaluate numerator and denominator', r'The numerator tends to $(-2)^3+2(-2)^2-1=-8+8-1=-1$. The denominator tends to $5-3(-2)=11\ne0$.'),
        ('(b) 应用商法则', r'因分母极限非零，原极限等于 $(-1)/11=-1/11$。', '(b) Apply the Quotient Law', r'The nonzero denominator limit permits division, giving $(-1)/11=-1/11$.')
    ], r'(a) $39$；(b) $-1/11$。', r'(a) $39$; (b) $-1/11$.', subpartIds=['a','b'])

example(3,'cancellation',102,
    r'求 $\lim_{x\to1}(x^2-1)/(x-1)$。', r'Find $\lim_{x\to1}(x^2-1)/(x-1)$.',
    [
        ('识别 $0/0$', r'代入 $x=1$ 得分子、分母都为 $0$，所以不能使用商法则直接代入。', 'Recognize $0/0$', r'Substitution gives zero in both numerator and denominator, so direct use of the Quotient Law is invalid.'),
        (r'分解并在 $x\ne1$ 时约分', r'$x^2-1=(x-1)(x+1)$，故当 $x\ne1$，$(x^2-1)/(x-1)=x+1$。', r'Factor and cancel for $x\ne1$', r'$x^2-1=(x-1)(x+1)$, so $(x^2-1)/(x-1)=x+1$ for $x\ne1$.'),
        ('求简式极限', r'$\lim_{x\to1}(x+1)=1+1=2$。原函数在 $1$ 无定义，仍可有极限 $2$。', 'Evaluate the simpler limit', r'$\lim_{x\to1}(x+1)=1+1=2$. The original function is undefined at 1 but still has limit 2.')
    ], '$2$', '$2$', graph={'numerator':[1,1],'denominator':[1],'bounds':{'xMin':-1,'xMax':3,'yMin':0,'yMax':4},'holes':[{'x':1,'y':2}]})

example(4,'cancellation',102,
    r'求 $\lim_{x\to1}g(x)$，其中 $g(x)=x+1$（$x\ne1$），$g(1)=\pi$。',
    r'Find $\lim_{x\to1}g(x)$, where $g(x)=x+1$ if $x\ne1$, and $g(1)=\pi$.',
    [
        ('把点值与附近行为分开', r'$g(1)=\pi$，但求极限考察的是 $x\ne1$ 且接近 $1$ 时的函数。', 'Separate the point value from nearby behavior', r'$g(1)=\pi$, but a limit examines nearby values with $x\ne1$.'),
        ('使用附近的表达式', r'在 $1$ 的去心邻域内 $g(x)=x+1$，所以两者极限相同。', 'Use the expression on the punctured neighborhood', r'$g(x)=x+1$ near 1 with $x\ne1$, so these functions have the same limit.'),
        ('代入得到极限', r'$\lim_{x\to1}g(x)=\lim_{x\to1}(x+1)=2$，与 $g(1)=\pi$ 不同。', 'Calculate the limit', r'$\lim_{x\to1}g(x)=\lim_{x\to1}(x+1)=2$, which differs from $g(1)=\pi$.')
    ], r'极限为 $2$；函数值为 $\pi$。', r'The limit is $2$; the function value is $\pi$.',
    graph={'numerator':[1,1],'denominator':[1],'bounds':{'xMin':-1,'xMax':3,'yMin':0,'yMax':4},'holes':[{'x':1,'y':2}],'points':[{'x':1,'y':3.141592653589793}]})

example(5,'difference-quotients',103,
    r'求 $\lim_{h\to0}((3+h)^2-9)/h$。', r'Evaluate $\lim_{h\to0}((3+h)^2-9)/h$.',
    [
        ('检查增量形式', r'$h=0$ 时原式无定义，极限中考虑 $h\ne0$。', 'Check the increment form', r'The original expression is undefined at $h=0$; the limit uses $h\ne0$.'),
        ('展开并提取 $h$', r'$(3+h)^2-9=9+6h+h^2-9=6h+h^2=h(6+h)$。', 'Expand and factor out $h$', r'$(3+h)^2-9=9+6h+h^2-9=6h+h^2=h(6+h)$.'),
        ('约分后求极限', r'当 $h\ne0$，商等于 $6+h$，所以 $\lim_{h\to0}(6+h)=6$。', 'Cancel and evaluate', r'For $h\ne0$ the quotient is $6+h$, so $\lim_{h\to0}(6+h)=6$.')
    ], '$6$', '$6$')

example(6,'rationalization',103,
    r'求 $\lim_{t\to0}(\sqrt{t^2+9}-3)/t^2$。', r'Find $\lim_{t\to0}(\sqrt{t^2+9}-3)/t^2$.',
    [
        ('识别根式差', r'原式为 $0/0$ 型，选择分子的共轭 $\sqrt{t^2+9}+3$。', 'Identify the radical difference', r'The expression has form $0/0$. Use the numerator conjugate $\sqrt{t^2+9}+3$.'),
        ('乘共轭并写出平方差', r'原式等于 $((t^2+9)-9)/(t^2(\sqrt{t^2+9}+3))=t^2/(t^2(\sqrt{t^2+9}+3))$。', 'Multiply and use the difference of squares', r'The quotient becomes $((t^2+9)-9)/(t^2(\sqrt{t^2+9}+3))=t^2/(t^2(\sqrt{t^2+9}+3))$.'),
        ('约分并代入', r'在 $t\ne0$ 时约去 $t^2$，得到 $1/(\sqrt{t^2+9}+3)$。分母趋于 $3+3=6\ne0$，所以极限为 $1/6$。', 'Cancel and substitute', r'Cancel $t^2$ for $t\ne0$, obtaining $1/(\sqrt{t^2+9}+3)$. The denominator tends to $3+3=6\ne0$, so the limit is $1/6$.')
    ], '$1/6$', '$1/6$')

example(7,'one-sided',104,
    r'证明 $\lim_{x\to0}|x|=0$。', r'Show that $\lim_{x\to0}|x|=0$.',
    [
        ('右侧改写绝对值', r'当 $x>0$，$|x|=x$，所以 $\lim_{x\to0^+}|x|=0$。', 'Rewrite on the right', r'For $x>0$, $|x|=x$, giving $\lim_{x\to0^+}|x|=0$.'),
        ('左侧改写绝对值', r'当 $x<0$，$|x|=-x$，所以 $\lim_{x\to0^-}|x|=0$。', 'Rewrite on the left', r'For $x<0$, $|x|=-x$, giving $\lim_{x\to0^-}|x|=0$.'),
        ('比较两侧', r'左右极限都为 $0$，故双侧极限存在且等于 $0$。', 'Compare the sides', r'Both one-sided limits equal $0$, so the two-sided limit exists and equals $0$.')
    ], '$0$', '$0$', solutionImage='assets/example-7-solution.png')

example(8,'one-sided',104,
    r'证明 $\lim_{x\to0}|x|/x$ 不存在。', r'Prove that $\lim_{x\to0}|x|/x$ does not exist.',
    [
        ('算右极限', r'当 $x>0$，$|x|/x=x/x=1$，所以右极限为 $1$。', 'Calculate the right-hand limit', r'For $x>0$, $|x|/x=x/x=1$, so the right-hand limit is $1$.'),
        ('算左极限', r'当 $x<0$，$|x|/x=(-x)/x=-1$，所以左极限为 $-1$。', 'Calculate the left-hand limit', r'For $x<0$, $|x|/x=(-x)/x=-1$, so the left-hand limit is $-1$.'),
        ('比较左右极限', r'$-1\ne1$，故双侧极限不存在。原式在 $x=0$ 无定义不是这个判断的依据；关键是两侧不同。', 'Compare the one-sided limits', r'Since $-1\ne1$, the two-sided limit does not exist. The decisive fact is the disagreement of the sides.')
    ], r'不存在：左极限 $-1$，右极限 $1$。', r'Does not exist: left limit $-1$, right limit $1$.',solutionImage='assets/example-8-solution.png')

example(9,'one-sided',104,
    r'若 $f(x)=\sqrt{x-4}$（$x>4$），$f(x)=8-2x$（$x<4$），判断 $\lim_{x\to4}f(x)$ 是否存在。',
    r'If $f(x)=\sqrt{x-4}$ for $x>4$ and $f(x)=8-2x$ for $x<4$, determine whether $\lim_{x\to4}f(x)$ exists.',
    [
        ('右侧使用根式分支', r'当 $x\to4^+$，$x-4\to0^+$，且 $\sqrt{x-4}\to0$。因此右极限为 $0$。', 'Use the radical branch on the right', r'As $x\to4^+$, $x-4\to0^+$ and $\sqrt{x-4}\to0$. The right-hand limit is $0$.'),
        ('左侧使用线性分支', r'$\lim_{x\to4^-}(8-2x)=8-2(4)=0$。', 'Use the linear branch on the left', r'$\lim_{x\to4^-}(8-2x)=8-2(4)=0$.'),
        ('比较并区分点值', r'左右都为 $0$，故双侧极限等于 $0$。题目没有定义 $f(4)$，但这不影响极限。', 'Compare and distinguish the point value', r'Both sides give $0$, so the two-sided limit is $0$. The problem leaves $f(4)$ undefined, which does not affect the limit.')
    ], r'存在，等于 $0$。', r'Exists and equals $0$.', solutionImage='assets/example-9-solution.png')

example(10,'floor',105,
    r'取整函数 $[x]$ 表示不大于 $x$ 的最大整数。证明 $\lim_{x\to3}[x]$ 不存在。',
    r'The greatest integer function is defined by $[x]=$ the largest integer less than or equal to $x$. Show that $\lim_{x\to3}[x]$ does not exist.',
    [
        ('从左侧靠近 3', r'当 $2\le x<3$，$[x]=2$，所以左极限为 $2$。', 'Approach 3 from the left', r'For $2\le x<3$, $[x]=2$, so the left-hand limit is $2$.'),
        ('从右侧靠近 3', r'当 $3\le x<4$，$[x]=3$，所以右极限为 $3$。', 'Approach 3 from the right', r'For $3\le x<4$, $[x]=3$, so the right-hand limit is $3$.'),
        ('比较两侧', r'$2\ne3$，因此双侧极限不存在；虽然函数值 $[3]=3$ 已定义。', 'Compare the two sides', r'$2\ne3$, so the two-sided limit does not exist, even though $[3]=3$ is defined.')
    ], r'不存在：左侧 $2$，右侧 $3$。', r'Does not exist: left $2$, right $3$.', solutionImage='assets/example-10-solution.png')

example(11,'squeeze',105,
    r'证明 $\lim_{x\to0}x^2\sin(1/x)=0$。', r'Show that $\lim_{x\to0}x^2\sin(1/x)=0$.',
    [
        ('不用不存在的振荡极限', r'$\sin(1/x)$ 在 $x\to0$ 时没有极限，不能直接使用乘积法则。对 $x\ne0$ 有 $-1\le\sin(1/x)\le1$。', 'Avoid the nonexistent oscillatory limit', r'$\sin(1/x)$ has no limit as $x\to0$, so the Product Law cannot be applied directly. For $x\ne0$, $-1\le\sin(1/x)\le1$.'),
        ('建立两侧界', r'因为 $x^2\ge0$，乘以 $x^2$ 保持不等号：$-x^2\le x^2\sin(1/x)\le x^2$。', 'Construct lower and upper bounds', r'Multiplication by $x^2\ge0$ preserves the inequalities: $-x^2\le x^2\sin(1/x)\le x^2$.'),
        ('求边界极限并夹逼', r'$\lim_{x\to0}(-x^2)=0=\lim_{x\to0}x^2$。由夹逼定理，中间函数的极限也为 $0$。', 'Evaluate the bounds and squeeze', r'$\lim_{x\to0}(-x^2)=0=\lim_{x\to0}x^2$. The Squeeze Theorem therefore gives limit $0$ for the middle function.')
    ], '$0$', '$0$', solutionImage='assets/example-11-solution.png',sourceEndPrintedPage=106,sourceEndPdfPage=138)

# Teaching associations are original pedagogical classifications, not publisher assignments.
mapping = {
    1: ([1,2], [60,61], '从给定极限或图像组合极限；拓展题检验法则条件。', 'Combine given or graph-read limits; extension problems test the hypotheses of the laws.'),
    2: ([3,4,5,6,7,8,9], [13,54,55,56,57,58], '直接代入并检查分母、根式条件；第13题检查商法则失效，其他拓展用于证明与应用。', 'Use substitution with denominator and radical checks; Exercise 13 checks a failure of the Quotient Law, and other extensions apply or prove the laws.'),
    3: ([11,12,15,16,19,20,24], [14,23,26,27,63], '分解并约去共同因子；拓展题综合通分、有理化、左右发散或参数分类。', 'Factor and cancel common factors; extensions add a common denominator, rationalization, one-sided divergence, or a parameter condition.'),
    4: ([10], [48,50,53], '区分附近表达式、点值和极限；拓展加入分段或取整函数。', 'Distinguish the nearby expression, point value, and limit; extensions involve piecewise or floor functions.'),
    5: ([17,18,28,31,32], [], '把增量差商展开或通分，约去增量再求极限。', 'Expand or combine an increment quotient, cancel the increment, and evaluate the limit.'),
    6: ([21,22,25,29,30,33,34], [62,64], '用共轭处理根式差；第62题处理两处根式差，第64题把几何截距化为根式差后有理化。', 'Use a conjugate for a radical difference; Exercise 62 handles two radical differences, and Exercise 64 rationalizes a radical difference arising from geometric intercepts.'),
    7: ([41], [43,44,47], '按符号改写绝对值；第43、44题综合约分并求指定单侧，第47题结合符号函数图像。', 'Rewrite absolute values by sign; Exercises 43 and 44 add cancellation and a specified one-sided limit, and Exercise 47 uses the sign-function graph.'),
    8: ([42,45,46,49], [47], '按左右符号分别改写；第45、46题只求指定的单侧极限，其余双侧问题还要比较两侧。', 'Rewrite according to the sign on each side. Exercises 45 and 46 ask only for the specified one-sided limit; two-sided questions also require comparing the sides.'),
    9: ([48,50], [49,54], '在每一侧使用对应分支；拓展结合绝对值或物理定义域。', 'Use the applicable branch on each side; extensions include absolute values or a physical domain.'),
    10: ([51], [52,53], '先确定整数区间；第52题综合复合函数，第53题用取整和观察跳跃抵消。', 'Identify the integer intervals; Exercise 52 adds a composition, and Exercise 53 uses a sum of floors to cancel jumps.'),
    11: ([35,36,37,38,39,40,59], [61], '建立趋于同一值的上下界；乘积反例说明振荡因子仍可能被压制。', 'Find bounds with the same limit; the product counterexample illustrates that oscillation can be suppressed.')
}
for q in examples:
    n = int(q['id'].split('-')[-1])
    same, extensions, reason, ereason = mapping[n]
    q['relatedExercises'] = [
        dict(number=k, relation=relation, reason=reason, en=dict(reason=ereason))
        for relation, numbers in [('same-method',same),('extension',extensions)] for k in numbers
    ]

# Crop only the source figures, with page provenance retained in the audit.
crops = {
    'example-1.png': (131,(110,953,320,1115)),
    'example-7-solution.png': (136,(45,247,281,395)),
    'example-8-solution.png': (136,(44,528,278,683)),
    'example-9-solution.png': (136,(44,961,289,1108)),
    'example-10-solution.png': (137,(108,162,335,376)),
    'example-11-solution.png': (138,(45,246,294,421)),
}
book = fitz.open(ROOT / 'James Stewart Calculus Early Transcendentals, 7th Edition 2012.pdf')
for filename,(page,box) in crops.items():
    clip = fitz.Rect(*(coordinate / 1.7 for coordinate in box))
    book[page-1].get_pixmap(matrix=fitz.Matrix(4,4),clip=clip).save(ASSETS / filename)

data = dict(course=COURSE, lesson=dict(
    id='2-3',section='2.3',title='用极限定律计算极限',
    description='8 个知识点、11 道教材例题与全部 64 道节后习题；按方法关联例题和练习，提供逐步解析。',
    en=dict(title='Calculating Limits Using the Limit Laws',
            description='8 concepts, all 11 textbook examples, and all 64 section exercises, with method-based links and step-by-step solutions.'),
    source=dict(kind='pdf',title='James Stewart · Calculus: Early Transcendentals, 7th Edition',
                printedPages=[99,108],pdfPages=[131,140]),
    concepts=concepts,questions=examples),
    textbook=dict(exercises=[]),
    coverage=json.loads((CONTENT / 'coverage-2-3.json').read_text(encoding='utf-8')),
    audit=dict(sourceReviewed=False,solutionsReviewed=False))
(CONTENT / 'section23-concepts-examples.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(concepts)} concepts; {len(examples)} examples')
