Names: George George, Antoine Tran
## Exercise 1 

1. Rewrite this requirement so it is testable, and list two questions you'd ask the author:
   *"Users should be able to reset their password easily."*
   Users should be able to reset their password without it being repeated. Two question for the author:
		   -  How should the user be verified?
		   - What are the validation checks for the password?
2. Classify each requirement as **functional** or **non-functional**:
    - (a) "The user can download an invoice as PDF." Functional(What the system does)
    - (b) "The app works on Chrome, Firefox and Safari." Non-Functional(How well the system does it)
    - (c) "The system sends an SMS when an order ships." Functional(What the system does)
3. Label each as **QA** or **QC**:
    - (a) Running test cases on a build - QC
    - (b) Introducing a code review checklist - QA
    - (c) Training developers on secure coding - QA
    - (d) Inspecting a release candidate for defects - QC
4. Label each as **verification** or **validation**:
    - (a) Reviewing the design document -Verification
    - (b) A customer trying the app in user acceptance testing - Validation
    - (c) A peer reviewing code against the spec - Verification
5. Identify the **error**, **defect**, and **failure**:
   *A developer thought VAT was 5% instead of 15% (**error**). The code calculates `price * 1.05`(**defect**). Customers' invoices show too little tax.* (**Failure**)

---

## Exercise 2 

1. Match each scenario to a testing principle:
    - (a) "We ran the same 50 tests for a year and found nothing new." *Principle 1*
    - (b) "Most bugs came from the payment module." *Principle 4*
    - (c) "The app passed every test, but users found it useless." *Principle 7*
2. Manual or automated?
    - (a) Checking a new logo looks right on mobile - *Manual*
    - (b) Running 400 regression tests every night - *Automated*
    - (c) Exploring a brand-new feature for the first time - *Manual*
3. Write **two positive** and **three negative** test cases for a "Sign up" form with Email and Password (password must be 8–16 characters).
		-  Positive test cases:
			- Valid email
			- Valid Password
		- Negative test cases:
			- Invalid email
			- Invalid password
			- "Email already exists" error
4. A movie ticket site gives prices by age: **0–12 = child, 13–59 = adult, 60+ = senior**. Identify the equivalence partitions (valid and invalid) and one test value for each.

| ID  | partition    | Type    | Representative | Expected   |
| --- | ------------ | ------- | -------------- | ---------- |
| T1  | Child, 0-12  | Valid   | 6              | 10         |
| T2  | Adult, 13-59 | Valid   | 40             | 17         |
| T3  | Senior, 60+  | Valid   | 80             | 15         |
| T4  | Negative     | Invalid | -6             | ValueError |
| T5  | Text         | Invalid | 'bomba'        | ValueError |
| T6  | Empty(None)  | Invalid | None           | ValueError |


---

## Exercise 3 

1. **BVA:** A text field accepts a username of **6 to 20 characters**. List the boundary values to test (three-value BVA) and the expected result for each.
	1. 3-value: 5(invalid), 6(valid), 7(valid), 19(valid), 20(valid), 21(invalid)
2. **Decision table:** A bank approves a loan if the applicant has a salary over $30,000 **and** a good credit score. Applicants with only one of these are sent for manual review. Applicants with neither are rejected. Build the decision table.

|                    | R1  | R2  | R3  | R4  |
| ------------------ | --- | --- | --- | --- |
| Salary over 30000  | T   | T   | T   | T   |
| Good credit score  | T   | T   | F   | F   |
| Neither of the two | F   | F   | F   | F   |

3. **State transition:** A document can go **Draft → Submitted → Approved**, or **Submitted → Rejected → Draft** (edited and resubmitted). List the valid transitions and one invalid transition to test.
	1. Valid transition:  Draft -> Submit -> Approved, Submit -> Rejected
	2. Invalid transitions: Draft -> Approved -> Submit
4. **Use case:** For "User withdraws cash from an ATM", write the main flow (4–6 steps) and two exception flows.
		- Step 1: User inserts card
		- Step 2: User is verified via PIN
		- Step 3: User selects the account for withdrawal
		- Step 4: User selects the amount for withdrawal
		- Step 5: System checks if the have sufficient funds
		- Step 6: ATM dispenses the money
		Exception Flows:
			- Incorrect pin
			- Insufficient funds
			- Beyond withdrawal limit
5. **Error guessing:** List five error-guessing tests for a "Phone number" field.
		- Wrong area code
		- Beyond the digit limit
		- Number doesn't exist
		- Special characters
		- Below the limit