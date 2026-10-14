# §2.3 Exercises 33–64: second independent review

Reviewed component: `content/section23-exercises-33-64.json`. This reviewer did not edit the author's component. The original questions were independently read from textbook PDF pages 139–140 / printed pages 107–108; the source boundary at Exercise 64 precedes the Section 2.4 heading.

## Scope and outcome

All 32 English prompts and written solutions were read and checked against their original expressions and requested cases. Independent numerical/algebraic checks focused on 33/34 table digits, 35/36 envelopes, 41–46 absolute-value limits, 52/53 exceptional floor values, and 62–64 algebra/geometry. No final-answer error was found. One proof-law condition in Exercise 36 was reported and corrected by the author; the corrected component was reread and verified.

This record does not set any whole-lesson review flag. The integrated site still needs its own rendering/interaction review.

## Detailed independent findings

| Exercises | Verified result and method |
| --- | --- |
| 33 | Rationalization gives (√(1+3x)+1)/3 → 2/3. All six table entries agree with direct evaluation of the original expression to their displayed 7 decimal places. The plotted curve has an open point at (0,2/3). |
| 34 | Rationalization gives 1/(√(3+x)+√3) → √3/6. All six table entries agree with direct evaluation to their displayed 7 decimal places. Rounding 0.288675… gives 0.29 and 0.2887 as requested; the graph's open point and height agree. |
| 35 | −x² ≤ x²cos(20πx) ≤ x², with both bounds → 0. The cosine frequency is correctly 20πx; the plot overlays the required three functions. |
| 36 | The radical covers x³+x² only; sin(π/x) is outside it. The amplitude is |x|√(1+x), real for x ≥ −1, with x ≠ 0 for the oscillating function. It tends to 0 because |x| → 0 and √(1+x) → 1; bounds ±|x|√(1+x) are valid on both sides near zero. |
| 37–38 | Bounds have common values 7 at x=4 and 2 at x=1, respectively. The x≥0 condition in 37 allows a full small neighborhood around 4. |
| 39–40 | Cosine is bounded by 1; the exponential of sine is between 1/e and e. Multiplication by x⁴ or √x provides valid shrinking bounds. Exercise 40 correctly uses x→0⁺. |
| 41 | Left formula x+3 and right formula 3x−3 both tend to 6. |
| 42 | Factor 2(x+6): left limit −2, right limit 2; no two-sided limit. |
| 43 | |2x³−x²| = x²|2x−1|. On the specified left approach to 0.5, the quotient equals −1/x² → −4. |
| 44 | A neighborhood of −2 is entirely negative, so |x|=−x on both sides. Cancellation gives 1 throughout the punctured neighborhood. |
| 45–46 | On the left the complete expression is 2/x → −∞; on the right it is identically zero. Divergent terms are combined before taking the limit. |
| 47 | Sign-function graph has open points at (0,±1) and a filled point at (0,0); limits are right 1, left −1, no two-sided sign limit, and absolute-sign limit 1. |
| 48 | Left/right limits at 1 are 2/1; the point value is 1, so the two-sided limit fails. Graph endpoints agree with the branch inequalities. |
| 49 | Factorization gives right branch x+3 and left branch −x−3. Right/left limits are 5/−5; both graph endpoints at x=2 are open. |
| 50 | At 1, both neighboring branch limits equal 1 while g(1)=3. At 2, left/right limits are −2/−1, so no two-sided limit exists. The isolated point and branch endpoints are correctly specified. |
| 51 | Floor at −2 has left/right limits −3/−2; at −2.4 the limit is −3. Integer n has side limits n−1/n. Two-sided limits exist at every noninteger. |
| 52 | Floor of cosine equals 0 near but not at x=0; f(0)=1. At π/2, side limits are 0/−1. Under the section's two-sided convention, interior a excluding ±π/2 have limits, including a=0. Inward endpoint limits are separately stated rather than mislabeled as two-sided. |
| 53 | Floor x + floor(−x) equals −1 immediately on both sides of 2, but its value at 2 is 0. |
| 54 | The real formula near c is defined only from v<c; its nonnegative radicand tends to zero, so observed length tends to zero. The revised solution explicitly justifies the square-root boundary by a positive-η inequality. |
| 55–56 | Finite polynomial sums follow from power/sum laws; rational substitution is restricted to q(a)≠0. |
| 57–58 | Multiplication by the vanishing x−1, x², or x yields limits 8, 0, and 0 without assuming point values at the excluded point. |
| 59 | The rational/irrational definition satisfies 0≤f(x)≤x² for all x; squeeze gives limit 0. |
| 60–61 | Opposite sign functions have sum 0 but neither individual limit. The sign function multiplied by itself has product limit 1 but no individual limits. Both counterexamples meet the full requirement. |
| 62 | Each radical difference equals (2−x) divided by its conjugate. The common factor cancels for x≠2, giving (√(3−x)+1)/(√(6−x)+2) → 1/2. |
| 63 | Finite-limit necessity is numerator value 15−a=0, hence uniquely a=15. Then numerator 3(x+2)(x+3) cancels against denominator (x+2)(x−1), and the limit is −1. |
| 64 | Circle equations independently yield Q=(r²/2, r√(1−r²/4)), 0<r<2. The line from P=(0,r) has slope 2(√(1−r²/4)−1)/r. Its x-intercept rationalizes to 2(1+√(1−r²/4)), approaching 4 from below; R→(4,0). |

## Graph and numerical evidence

- Solution images for **33–36** were individually viewed. Their formula labels, envelopes, omitted original point values, and highlighted limiting heights agree with the written mathematics.
- The original figure for **64** was individually viewed: the fixed circle is centered at (1,0), the shrinking circle is centered at the origin, P is above the origin, and Q is the upper intersection. The figure's line and R position are consistent with the derived positive intercept.
- Extracted all 12 actual displayed table entries in 33/34 and independently evaluated the original question formulas. Maximum allowed discrepancy was 5.1×10⁻⁸ (half a unit in the last displayed decimal, allowing floating-point roundoff); every entry passed.
- Evaluated 35/36 at **1000 nonzero sample points** in [−0.5,0.5]. Every inequality passed, as did √(x³+x²)=|x|√(1+x). These checks supplement the symbolic inequality proof; they are not claimed as proof by themselves.
- Checked original expressions in 41–46 at distances 10⁻², 10⁻³, 10⁻⁴ on the applicable side(s). Exact side formulas and signs agree.
- Checked original and independently simplified expressions in 62/63 at the same three distances. The pairs approach 1/2 and −1 respectively and the identities agree within floating-point error.
- Recomputed 64 at **50 decimal digits** for r=1, 0.1, 0.01, 0.001, 0.0001. Q satisfies both circles, and the x-intercept derived directly from the line agrees with the conjugate formula. Intercepts are approximately 3.73205, 3.997498, 3.999975, 3.99999975, 3.9999999975, confirming approach to 4 from below.
- Checked neighboring floor values in 52/53 independently to avoid treating isolated point values as limits.

Executable check and compact evidence are in `tmp/exercises-a/check_second_component.py` and `tmp/exercises-a/second-component-checks.txt`.

## Reported issue and verified correction

Exercise 36 initially cited the chapter's Root Law directly at limiting radicand zero, even though the stated even-root law requires a positive radicand limit. The author changed the argument in both languages to the factorization |x|√(1+x), so only the positive limit 1 is passed through the Root Law and the product tends to 0. The fresh component was inspected and this correction is present. Exercises 40 and 54 were also strengthened with explicit inequalities proving a nonnegative square root tends to zero.

No remaining mathematical finding arose from this review's scope.
