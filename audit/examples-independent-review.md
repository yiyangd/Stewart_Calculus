# §2.3 Examples and exercise links: independent review

Reviewed component: `content/section23-concepts-examples.json`. This record is an independent mathematical/source review, not a whole-lesson approval flag. No other author's JSON was modified during the review.

## Original pages visually inspected

- PDF 131 / printed 99: section title, basic limit-law hypotheses, Example 1 question and its original graph.
- PDF 132 / printed 100: all three Example 1 solutions, power/basic/root laws.
- PDF 133 / printed 101: Example 2(a,b), general root-law hypothesis, direct substitution statement.
- PDF 134 / printed 102: Examples 3 and 4, factor cancellation, equality on a punctured neighborhood, both related graphs.
- PDF 135 / printed 103: Examples 5 and 6, one-sided characterization.
- PDF 136 / printed 104: Examples 7, 8, and 9, including exact branch inequalities.
- PDF 137 / printed 105 and PDF 138 / printed 106: Examples 10 and 11, greatest-integer notation and squeeze proof.
- PDF 138–140 / printed 106–108: every original exercise number targeted by a `relatedExercises` link.

Every listed page was read as an image, not just from extracted text. Source positions recorded in the example records agree with their starting page; Example 11 correctly continues on the following page.

## Example mathematics and English source fidelity

| Example | Independently verified conclusion | Notes |
| --- | --- | --- |
| 1(a) | 1 + 5(−1) = −4 | Graph limit at −2 is used rather than the filled-point value. |
| 1(b) | Product left/right limits −4/−2; no two-sided limit | f tends to 2 on both sides; g tends to −2/−1. |
| 1(c) | Quotient left/right limits −∞/+∞ | The original graph has g < 0 immediately left of 2, g > 0 immediately right; f tends to approximately 1.4 > 0. Direction is established by this graph, not inferred merely from a zero denominator. |
| 2(a) | 2(25) − 3(5) + 4 = 39 | Polynomial powers and all constant signs agree with the textbook. |
| 2(b) | (−8 + 8 − 1)/(5 + 6) = −1/11 | Denominator limit 11 is nonzero. |
| 3 | 2 | x²−1 = (x−1)(x+1), with x ≠ 1 before canceling. |
| 4 | Limit 2, point value π | The defined exceptional point does not alter nearby values. |
| 5 | 6 | (3+h)²−9 = h(6+h), with h ≠ 0 before cancellation. |
| 6 | 1/6 | The denominator is t², not t; rationalization gives 1/(√(t²+9)+3). |
| 7 | 0 | Left/right forms −x/x both tend to zero. |
| 8 | No two-sided limit; left −1, right 1 | Undefined value at zero is distinguished from failure of the limit. |
| 9 | 0 | Right branch √(x−4), x>4; left branch 8−2x, x<4. Both tend to 0, and f(4) is left undefined. |
| 10 | No two-sided limit; left 2, right 3 | Floor is greatest integer ≤ x; the point value [3] = 3 is correct. |
| 11 | 0 | −x² ≤ x² sin(1/x) ≤ x²; no illicit product of 0 with a nonexistent oscillatory limit. |

All 11 English prompts preserve the original requested operations, approach points, signs, and cases. Examples 1 and 2 include all their lettered subparts. Explanations and final answers agree in the two languages. All reviewed concept statements correctly retain the nonzero-denominator condition and the textbook's positive limiting-radicand condition for even roots.

## Audit of every example-to-exercise association

The mapping table below records the reviewed links. “Same method” is acceptable when the exercise's principal solution method is the displayed example's method, even if a routine preparatory expansion/common denominator is added. A change in the decisive limit behavior, or a different substantial preparatory method, belongs under “Extension.”

| Example | Same-method links judged sound | Extension links judged sound | Corrections or refinements |
| --- | --- | --- | --- |
| 1 | 1, 2 | 60, 61 | Graph/component law exercises are direct matches; counterexamples test the limits of the component laws. |
| 2 | 3, 4, 5, 6, 7, 8, 9 | 13, 54, 55, 56, 57, 58 | **13 was corrected to Extension**, because its denominator tends to zero while its numerator tends to 6; direct substitution does not yield a finite answer. |
| 3 | 11, 12, 15, 16, 19, 20, 24 | 14, 23, 26, 27, 63 | **14 was corrected to Extension**, because cancellation leaves x/(x+1), whose denominator still tends to zero, followed by opposite one-sided infinities. 27's rationalization is correctly marked Extension. 23/26 add common-denominator preparation. |
| 4 | 10 | 48, 50, 53 | These extensions require additional piecewise/floor analysis; they share the point-value versus limit distinction. |
| 5 | 17, 18, 28, 31, 32 | — | All are difference quotients; reciprocal cases use a common denominator in place of polynomial expansion. Fixed parameters and their domains must remain explicit. |
| 6 | 21, 22, 25, 29, 30, 33, 34 | 62, 64 | Conjugate multiplication is decisive throughout; 29 first combines terms, 62 needs two conjugates, and 64 first derives the geometric intercept. |
| 7 | 41 | 43, 44, 47 | **43 and 44 were corrected to Extension**: 43 additionally factors and cancels a 0/0 form and asks only for a left-hand limit; 44 applies the correct absolute-value branch then cancels x+2. |
| 8 | 42, 45, 46, 49 | 47 | Valid sign-based rewrites. 45/46 ask only for the specified side, while 49 also uses routine factorization of its polynomial numerator. |
| 9 | 48, 50 | 49, 54 | Piecewise branch analysis is direct; the absolute-value expression and physical-domain boundary are extensions. |
| 10 | 51 | 52, 53 | Composition and cancellation of floor jumps extend the basic integer-jump example. |
| 11 | 35, 36, 37, 38, 39, 40, 59 | 61 | All same-method items use common-limit bounds; 36 also checks local nonnegative radicands. The product counterexample is a conceptual extension. |

At the initial reading, 13 under Example 2 and 14 under Example 3 were still labeled `same-method`; these corrections were reported to the integrator, who owns the source component. 27 under Example 3 was already correctly labeled `extension`. The two suggested refinements under Example 7 were also reported. A fresh read verified that all four reported classification changes are now present; they do not change any numerical answer.

Three exercises, 23, 26, and 64, were not listed under an example in the initial mapping. The integrator added Example 3 → 23/26 as extensions (common-denominator preparation followed by cancellation), and Example 6 → 64 as an extension (geometric setup followed by conjugate simplification). A fresh read verified all three added links. Every exercise from 1 through 64 now has an example route in addition to its concept association.

## Review status

- All example questions and mathematical solutions: independently checked, no mathematical correction needed.
- All present related-exercise targets: checked against their original source expressions and required limit methods.
- Mapping corrections/refinements: communicated to the integrator and verified in the updated source; this reviewer did not alter the other component.
- Exercise 33–64 solution review: recorded separately in `audit/exercises-33-64-second-review.md`.
