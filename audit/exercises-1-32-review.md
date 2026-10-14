# §2.3 Exercises 1–32: source and solution review

This is a component review record. It does **not** set or authorize the whole-lesson `sourceReviewed` or `solutionsReviewed` flags. A separate integrator must inspect this component in the complete lesson.

## Original source examined visually

- Textbook: *James Stewart, Calculus: Early Transcendentals*, 7th edition (2012), PDF page **138**, printed page **106**: exercises 1–10; all six subparts of 1 and 2; both subparts of 10; both given graphs in 2.
- Textbook PDF page **139**, printed page **107**: exercises **11–32** and the original heading “Evaluate the limit, if it exists.”
- These two full-page renders were inspected with the image-viewing tool. The mathematical expressions were read from the page images, using extracted text only as secondary assistance.
- The figure in exercise 2 was located in `tmp/source/textbook-138.png`, rectangle `(72, 848, 427, 982)` in the original 1037×1201 render (scale 1.7). The corresponding PDF rectangle was extracted directly at scale 4 for crisp linework and readable labels. The crop includes only the two given coordinate plots. The completed crop was itself viewed and checked for complete axes, unit labels, open circles, and filled points.

## Answer reference examined visually

- Answer book PDF **97**, printed **87**: exercises 1–3.
- Answer book PDF **98**, printed **88**: exercises 4–8.
- Answer book PDF **99**, printed **89**: exercises 9–20.
- Answer book PDF **100**, printed **90**: exercises 21–29.
- Answer book PDF **101**, printed **91**: exercises 30–32 (the other material on that page was outside this component).
- All five page images were inspected directly. The answer reference was used to cross-check results; the bilingual explanations, domain remarks, and detailed arithmetic were written for this lesson independently.

## Coverage and bilingual checks

- JSON array contains exactly **32** records in source order, numbered 1 through 32.
- The independently observed subparts are 1(a–f), 2(a–f), and 10(a–b). Their `subpartIds`, written steps, and final answers include every subpart.
- Every exercise records printed/PDF pages 106/138 or 107/139 as appropriate.
- Every displayed prompt, step, and answer has a matching English field; Chinese and English step counts agree.
- Exercises 3–9 identify the applicable laws explicitly, as the original heading requires.
- The graph for exercise 2 is supplied as `assets/exercise-2.png` and must remain visible in the question, before opening the solution.
- The component contains no review-completion flags.

## Mathematical review methods

1. Recomputed 1(a–d,f) with the stated sum, power, root, quotient, and product laws. Checked the nonzero denominator conditions and the positive radicand in 1(c).
2. Read the graph in 2 separately: at 2, the limit of f is 2 but its actual value is 1; the limit of g is 0. At 1, f tends to 1, while g has left/right limits 2/1. At −1, f tends to −1, and g crosses zero from negative to positive.
3. Expanded and factored the polynomial and difference-quotient expressions; recomputed all arithmetic in the cancellation and substitution steps.
4. Verified each conjugate operation by the identity `(A−B)(A+B)=A²−B²`, including the signs in 25, 27, 29, and 30.
5. Ran independent evaluations of the **original question expressions** near the limiting point for exercises 3–9, 11–12, and 15–30. Symmetric evaluations at distance 10⁻⁴ agreed with the written exact results within 2×10⁻⁴; distances were kept moderate to avoid false failure from subtractive floating-point cancellation. This numerical evidence supplements the symbolic derivations; it does not replace them.
6. Checked 31 and 32 at fixed x = −2, −0.5, 1, 3 from both sides in h. Results agree with 3x² and −2/x³, respectively.
7. Checked the signs and growth in 13 and 14 at distances 10⁻², 10⁻³, 10⁻⁴ on both sides, and confirmed the symbolic sign analysis.
8. Ran component checks for contiguous exercise numbering, required fields, equal bilingual step counts, concept IDs, page correspondence, exact subpart lists, image existence, paired math delimiters, and absence of invisible control characters or public local paths.

The verification command is recorded in `tmp/exercises-a/check_exercises.py`; compact numerical evidence is in `tmp/exercises-a/numerical-checks.txt`.

## Special issues and deliberate clarifications

- **1(e):** A zero denominator limit and nonzero numerator limit exclude a finite limit on the quotient's approaching domain. The supplied limits do not determine a unique +∞ or −∞ direction. The solution gives three admissible h examples with different behavior, instead of inventing a direction. If h vanishes identically on a neighborhood, the quotient itself has no such approaching domain; no finite limit can be asserted from the question in that case either.
- **2(b):** The sum's left limit is **3**, and right limit is **2**. Saying only “g has no limit” would omit a useful direct check of the sum itself.
- **2(c):** g's height at zero is finite but cannot be inferred as an exact algebraic number from the plot. The solution denotes it by L and uses 0·L = 0; no invented exact height is needed.
- **2(d):** The quotient has left/right limits **+∞/−∞**, so the two-sided limit does not exist.
- **13:** Numerator tends to 6, not 0; left/right limits are **−∞/+∞**. Cancellation of x−5 is unavailable.
- **14:** A common x−4 factor can be canceled near −1, but x+1 still tends to zero. Left/right limits are **+∞/−∞**.
- **24:** Only one x+1 factor cancels; the remaining numerator tends to zero, giving limit 0.
- **26 and 29:** Separate subtraction of divergent terms is invalid. Combine the terms before taking limits.
- **31 and 32:** h is the variable tending to zero; x is a fixed parameter. Exercise 32 requires **x ≠ 0**, and the original expression is undefined at x = 0. This condition is stated in both languages.

## Deliverable paths

- `content/section23-exercises-1-32.json`
- `content/assets/exercise-2.png`
- `audit/exercises-1-32-review.md`
