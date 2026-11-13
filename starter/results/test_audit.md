# Test audit — metadata và grounding (6 câu test × A/B/C × top-3)

Metadata: so `source`, `page`, `chapter` của từng kết quả với PDF. Cột auto-check chỉ là trợ giúp:
text chunk có nằm đúng ở trang ghi trong metadata không, và chapter có khớp mục lục không.
Grounding (cho cả top-3 của một câu): 0 = không có bằng chứng; 1 = có nhưng thiếu điều kiện/ngữ cảnh;
2 = đủ để trả lời và truy nguồn.

> **Nhãn do AI (Claude) đề xuất, tác giả Trần Văn Tài đã duyệt và giữ nguyên (2026-11-13).** Claude đọc top-3 trong trace và so với PDF; người chấm biết kết quả Hit@k trước khi chấm (nguy cơ thiên lệch).
>
> Quy tắc grounding: 2 = top-3 có bằng chứng đủ trả lời theo ngữ cảnh câu hỏi (chương được cung cấp); 1 = có bằng chứng nhưng thiếu một phần (lý do/điều kiện), chỉ gián tiếp, hoặc bị đoạn mâu thuẫn từ chương khác xếp trên; 0 = không có bằng chứng cho đúng nghĩa câu hỏi.

## A · q21 (paraphrase) — How does Python show that one decision statement is placed inside another?
- Gold: trang 116; filter yêu cầu: None; filter áp dụng: None
- Evidence: "Nesting allows a decision statement to be inside another decision statement, and is indicated by an indentation level."
- Tự động: Hit@1=False, Evidence Hit@3=False

### #1 `openstax-intro-python:p095:A:00` score=0.530389
- source=data/raw/intro-python-programming.pdf · page=95 · chapter=4 · book_page=None
- auto-check: text_on_page=True, chapter_matches_toc=True
    Figure 4.1 credit: modification of work "Fork In The Road", by Ian Sane/Flickr, CC BY 2.0
    Chapter Outline
    4.1 Boolean values
    4.2 If-else statements
    4.3 Boolean operations
    4.4 Operator precedence
    4.5 Chained decisions
    4.6 Nested decisions
    4.7 Conditional expressions
    4.8 Chapter summary
    Introduction
    The Python interpreter follows a single path of execution when executing a program. What if a programmer
    wants to define multiple possible paths? Ex: Instead of always taking the left path, a program u

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p116:A:01` score=0.496949
- source=data/raw/intro-python-programming.pdf · page=116 · chapter=4 · book_page=106
- auto-check: text_on_page=True, chapter_matches_toc=True
    h nested if-else statements.
    Nested decision statements
    Suppose a programmer is writing a program that reads in a game ID and player count and prints whether the
    user has the right number of players for the game.
    The programmer may start with:
    if game == 1 and players < 2:
    print("Not enough players")
    if game == 1 and players > 4:
    print("Too many players")
    if game == 1 and (2 <= players <= 4):
    print("Ready to start")
    if game == 2 and players < 3:
    print("Not enough players")
    if game == 2 and playe

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p154:A:03` score=0.483554
- source=data/raw/intro-python-programming.pdf · page=154 · chapter=6 · book_page=144
- auto-check: text_on_page=True, chapter_matches_toc=True
    ction-python-programming/pages/
    6-2-control-flow)
    TRY IT
    TRY IT

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding A·q21 (0/1/2):** 0
**Lý do:** Không chunk nào nêu nesting được biểu thị bằng thụt lề. p116:A:01 chỉ có phần mở đầu ví dụ game/players, câu 'indicated by an indentation level' nằm ở chunk khác; p95 và p154 không liên quan.

---

## A · q22 (direct) — What is a loop with no termination condition called, and what statement lets it stop?
- Gold: trang 138; filter yêu cầu: None; filter áp dụng: None
- Evidence: "A break statement is an essential part of a loop that does not have a termination condition. A loop without a termination condition is known as an infinite loop."
- Tự động: Hit@1=False, Evidence Hit@3=True

### #1 `openstax-intro-python:p143:A:02` score=0.598617
- source=data/raw/intro-python-programming.pdf · page=143 · chapter=5 · book_page=133
- auto-check: text_on_page=True, chapter_matches_toc=True
     or a while loop to allow the program execution to exit the loop
    once a given condition is triggered.
    • A continue statement allows for skipping the execution of the remainder of the loop without exiting the
    loop entirely.
    • A loop else statement runs after the loop's execution is completed without being interrupted by a break
    statement.
    At this point, you should be able to write programs with loop constructs. The programming practice below ties
    together most topics presented in the chapter.
    Fun

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p138:A:00` score=0.591084
- source=data/raw/intro-python-programming.pdf · page=138 · chapter=5 · book_page=128
- auto-check: text_on_page=True, chapter_matches_toc=True
    INFINITE LOOP
    A break statement is an essential part of a loop that does not have a termination condition. A loop without
    a termination condition is known as an infinite loop. Ex: An infinite loop that counts up starting from 1 and
    prints the counter's value while the counter's value is less than 10. A break condition is triggered when the
    counter's value is equal to 10, and hence the program execution exits.
    counter = 1
    while True:
    if counter >= 10:
    break
    print(counter)
    counter += 1
    CONCEPTS IN

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p141:A:00` score=0.583351
- source=data/raw/intro-python-programming.pdf · page=141 · chapter=5 · book_page=131
- auto-check: text_on_page=True, chapter_matches_toc=True
    statement. A loop else is used to identify if the loop is terminated normally or the execution is interrupted by
    a break statement.
    Ex: A for loop that iterates over a list of numbers to find if the value 10 is in the list. In each iteration, if 10 is
    observed, the statement "Found 10!" is printed and the execution can terminate using a break statement. If
    10 is not in the list, the loop terminates when all integers in the list are evaluated, and hence the else
    statement will run and print "10 i

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding A·q22 (0/1/2):** 2
**Lý do:** p138:A:00 chứa trọn 'A break statement is an essential part of a loop that does not have a termination condition... known as an infinite loop'. #1 p143 (tóm tắt break) cùng chương, không mâu thuẫn.

---

## A · q23 (metadata_filter) — In what situation is the else clause executed?
- Gold: trang 141 (hoặc [143]); filter yêu cầu: {'chapter': 5}; filter áp dụng: None
- Evidence: "A loop else is used to identify if the loop is terminated normally or the execution is interrupted by a break statement."
- Tự động: Hit@1=False, Evidence Hit@3=False

### #1 `openstax-intro-python:p102:A:01` score=0.568474
- source=data/raw/intro-python-programming.pdf · page=102 · chapter=4 · book_page=92
- auto-check: text_on_page=True, chapter_matches_toc=True
    ay, we'll walk. Else, we'll
    drive.
    An else statement is used with an if statement and contains a body of statements that is executed when the
    if statement's condition is false. When an if-else statement is executed, one and only one of the branches
    is taken. That is, the body of the if or the body of the else is executed. Note: The else statement is at the
    same level of indentation as the if statement, and the body is indented.
    if-else statement template:
    1 # Statements before
    2
    3 if condition:
    

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p102:A:02` score=0.563784
- source=data/raw/intro-python-programming.pdf · page=102 · chapter=4 · book_page=92
- auto-check: text_on_page=True, chapter_matches_toc=True
    template:
    1 # Statements before
    2
    3 if condition:
    4 # Body
    5 else:
    6 # Body
    7
    8 # Statements after
    CHECKPOINT
    Example: Trivia question
    Example: Trivia question; ch 4, video 5 (https://www.openstax.org/r/trivia-question)
    CONCEPTS IN PRACTICE
    Exploring if-else statements
    6 . Given the following code, the else branch is taken for which range of x?

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p123:A:00` score=0.525191
- source=data/raw/intro-python-programming.pdf · page=123 · chapter=4 · book_page=113
- auto-check: text_on_page=True, chapter_matches_toc=True
    Function Description
    elif statement
    # Statements before
    if condition:
    # Body
    elif condition:
    # Body
    else:
    # Body
    # Statements after
    Nested if
    statement
    # Statements before
    if condition:
    if condition:
    # Body
    else:
    # Body
    else:
    if condition:
    # Body
    else:
    # Body
    # Statements after
    Conditional
    expression
    expression_if_true if condition else expression_if_false
    Table 4.5 Chapter 4 reference.

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding A·q23 (0/1/2):** 0
**Lý do:** Cả 3 chunk thuộc chương 4 (if-else, p102, p123), trả lời sai nghĩa 'else' so với ngữ cảnh chương 5 (loop else). Không có bằng chứng về loop else.

---

## A · q24 (exception) — A function normally treats a variable it edits as local. How can it modify a global variable instead?
- Gold: trang 157; filter yêu cầu: None; filter áp dụng: None
- Evidence: "To edit a global variable inside a function, the variable must be declared with the global keyword."
- Tự động: Hit@1=False, Evidence Hit@3=True

### #1 `openstax-intro-python:p157:A:02` score=0.667246
- source=data/raw/intro-python-programming.pdf · page=157 · chapter=6 · book_page=147
- auto-check: text_on_page=True, chapter_matches_toc=True
    Editing global variables in a program with a function; ch 6, video 8 (https://www.openstax.org/r/editing-
    global-variables)

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p157:A:01` score=0.572044
- source=data/raw/intro-python-programming.pdf · page=157 · chapter=6 · book_page=147
- auto-check: text_on_page=True, chapter_matches_toc=True
    rint_greeting() and print_time()
    Using local and global variables together
    Python allows global and local variables to have the same name, which can lead to unexpected program
    behavior. A function treats a variable edited within the function as a local variable unless told otherwise. To edit
    a global variable inside a function, the variable must be declared with the global keyword.
    CHECKPOINT
    Editing global variables in a program with a function
    Editing global variables in a program with a funct

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p156:A:01` score=0.519583
- source=data/raw/intro-python-programming.pdf · page=156 · chapter=6 · book_page=146
- auto-check: text_on_page=True, chapter_matches_toc=True
     executing, the
    function's local variables no longer exist.
    CHECKPOINT
    Global and local variables in a program with a function
    Global and local variables in a program with a function; ch 6, video 7 (https://www.openstax.org/r/global-
    and-local-variables)
    CONCEPTS IN PRACTICE
    Local variables
    4 . Which variables are local?
    def print_time():
    out_str = "Time is " + str(hour) + ":" + str(min)
    print(out_str)
    hour = int(input())
    min = int(input())
    print_time()
    a. hour and min
    b. out_str
    c. hour, min, a

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding A·q24 (0/1/2):** 2
**Lý do:** #2 p157:A:01 chứa trọn 'To edit a global variable inside a function, the variable must be declared with the global keyword.' #1 chỉ là link video (nhiễu).

---

## A · q25 (exception) — Why should a list not be used as a default parameter value?
- Gold: trang 170; filter yêu cầu: None; filter áp dụng: None
- Evidence: "Note: Default parameter values are only defined once to be used by the function, so mutable objects (such as lists) should not be used as default values."
- Tự động: Hit@1=False, Evidence Hit@3=False

### #1 `openstax-intro-python:p160:A:01` score=0.39627
- source=data/raw/intro-python-programming.pdf · page=160 · chapter=6 · book_page=150
- auto-check: text_on_page=True, chapter_matches_toc=True
    a programmer wants to write a function that prints the contents of a list? Good practice is to pass
    values directly to a function rather than relying on global variables. A function argument is a value passed as
    input during a function call. A function parameter is a variable representing the input in the function
    definition. Note: The terms "argument" and "parameter" are sometimes used interchangeably in conversation
    and documentation.
    CHECKPOINT
    Global and local variables in a program with a f

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p170:A:01` score=0.390683
- source=data/raw/intro-python-programming.pdf · page=170 · chapter=6 · book_page=160
- auto-check: text_on_page=True, chapter_matches_toc=True
     (such as
    lists) should not be used as default values.
    The physics example below calculates weight as a force in newtons given mass in kilograms and acceleration
    in . Gravity on Earth is 9.8 , and gravity on Mars is 3.7 .
    CHECKPOINT
    Using default parameter values
    Using default parameter values; ch 6, video 14 (https://www.openstax.org/r/default-parameter-values)
    CONCEPTS IN PRACTICE
    Using default parameter values
    Consider the following updated version of greeting():
    def greeting(msg, name="Frien

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p171:A:03` score=0.353324
- source=data/raw/intro-python-programming.pdf · page=171 · chapter=6 · book_page=161
- auto-check: text_on_page=True, chapter_matches_toc=True
     the arguments' values.
    • Function calls can use positional arguments to map values to parameters in order.
    • Function calls can use keyword arguments to map values using parameter names in any order.
    • Functions can define default parameter values to allow for optional arguments in function calls.
    • Python uses a pass-by-object-reference system to assign parameters with the object values referenced by
    the arguments.
    • Functions can use return statements to return values back to the calling code

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding A·q25 (0/1/2):** 1
**Lý do:** p170:A:01 bắt đầu giữa câu '(such as lists) should not be used as default values' — có kết luận nhưng mất lý do 'defined only once'. Không chunk nào khác bổ sung lý do.

---

## A · q26 (metadata_filter) — Should there be spaces around the equals sign according to PEP 8?
- Gold: trang 171; filter yêu cầu: {'chapter': 6}; filter áp dụng: None
- Evidence: "The PEP 8 style guide recommends no spaces around = when indicating keyword arguments and default parameter values."
- Tự động: Hit@1=False, Evidence Hit@3=True

### #1 `openstax-intro-python:p110:A:02` score=0.506637
- source=data/raw/intro-python-programming.pdf · page=110 · chapter=4 · book_page=100
- auto-check: text_on_page=True, chapter_matches_toc=True
    cing around operators to avoid extraneous and confusing
    whitespace.
    • Avoid multiple spaces and an unequal amount of whitespace around operators with two operands.
    Avoid: x= y * 44
    Better: x = y * 44
    • Avoid spaces immediately inside parentheses.
    Avoid: x = ( 4 * y )
    Better: x = (4 * y)
    • Surround the following operators with one space: assignment, augment assignment, comparison,

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p110:A:01` score=0.480558
- source=data/raw/intro-python-programming.pdf · page=110 · chapter=4 · book_page=100
- auto-check: text_on_page=True, chapter_matches_toc=True
    om what the programmer
    wanted?
    a. Equality has precedence over and.
    b. All operators are evaluated right to left.
    c. Order is random when parentheses aren't used.
    8 . Given x = 8 and y = 9, what is the result of the following?
    x + 3 * y - 5
    a. 30
    b. 44
    c. 94
    9 . Given x = 8 and y = 9, what is the result of the following?
    (x+3) * (y-5)
    a. 30
    b. 44
    c. 94
    PEP 8 RECOMMENDATIONS: SPACING AROUND OPERATORS
    The PEP 8 style guide recommends consistent spacing around operators to avoid extraneous and conf

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p171:A:00` score=0.449521
- source=data/raw/intro-python-programming.pdf · page=171 · chapter=6 · book_page=161
- auto-check: text_on_page=True, chapter_matches_toc=True
    PEP 8 RECOMMENDATIONS: SPACING
    The PEP 8 style guide recommends no spaces around = when indicating keyword arguments and default
    parameter values.
    Stream donations
    Write a function, donate(), that lets an online viewer send a donation to a streamer. donate() has three
    parameters:
    • amount: amount to donate, default value: 5
    • name: donor's name, default value: "Anonymous"
    • msg: donor's message, default value: ""
    Given:
    donate(10, "gg")
    The output is:
    Anonymous donated 10 credits: gg
    Write funct

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding A·q26 (0/1/2):** 1
**Lý do:** #3 p171:A:00 có đáp án đúng (không cách quanh = với keyword/default), nhưng #1 p110 (chương 4) xếp trên và nói 'Surround ... assignment ... with one space' — mâu thuẫn; thiếu điều kiện ngữ cảnh để chọn.

---

## B · q21 (paraphrase) — How does Python show that one decision statement is placed inside another?
- Gold: trang 116; filter yêu cầu: None; filter áp dụng: None
- Evidence: "Nesting allows a decision statement to be inside another decision statement, and is indicated by an indentation level."
- Tự động: Hit@1=False, Evidence Hit@3=False

### #1 `openstax-intro-python:p095:B:01` score=0.519051
- source=data/raw/intro-python-programming.pdf · page=95 · chapter=4 · book_page=None
- auto-check: text_on_page=True, chapter_matches_toc=True
    Introduction
    The Python interpreter follows a single path of execution when executing a program. What if a programmer
    wants to define multiple possible paths? Ex: Instead of always taking the left path, a program uses the path
    width to decide which path to take. If the left path is wider, take the right path. Else, take the left path.
    A branch is a group of statements that execute based on a condition. The Expressions chapter introduced
    expressions. This chapter explores how expressions can be used as conditions to make decisions in programs.

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p111:B:02` score=0.496923
- source=data/raw/intro-python-programming.pdf · page=111 · chapter=4 · book_page=101
- auto-check: text_on_page=True, chapter_matches_toc=True
    Two separate if statements do not guarantee that only one branch is taken and might result in both branches
    being taken. Ex: The program below attempts to add a curve based on the input test score. If the input is 60,
    both if statements are incorrectly executed, and the resulting score is 75.
    score = int(input())
    if score < 70:
    score += 10
    # Wrong:
    if 70 <= score < 85:
    score += 5
    Chaining decision statements with elif allows the programmer to check for multiple conditions. An elif (short
    for else if) statement checks a condition when the prior decision statement's condition is false. An elif
    statement is part of a chain and must follow an if (or elif) statement.
    if-elif statement template:
    # Statements before
    if condition:
    # Body
    elif condition:
    # Body
    # Statements after

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p100:B:02` score=0.484264
- source=data/raw/intro-python-programming.pdf · page=100 · chapter=4 · book_page=90
- auto-check: text_on_page=True, chapter_matches_toc=True
    A condition is an expression that evaluates to true or false. An if statement is a decision-making structure
    that contains a condition and a body of statements. If the condition is true, the body is executed. If the
    condition is false, the body is not executed.
    The if statement's body must be grouped together and have one level of indentation. The PEP 8 style guide
    recommends four spaces per indentation level. The Python interpreter will produce an error if the body is
    empty.
    TRY IT
    TRY IT

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding B·q21 (0/1/2):** 1
**Lý do:** Không có trang 116. p100:B:02 nói thân if 'have one level of indentation' — liên quan gián tiếp (câu lồng nằm trong thân nên thụt lề) nhưng không nói về nesting; phải tự suy luận.

---

## B · q22 (direct) — What is a loop with no termination condition called, and what statement lets it stop?
- Gold: trang 138; filter yêu cầu: None; filter áp dụng: None
- Evidence: "A break statement is an essential part of a loop that does not have a termination condition. A loop without a termination condition is known as an infinite loop."
- Tự động: Hit@1=True, Evidence Hit@3=True

### #1 `openstax-intro-python:p138:B:00` score=0.59176
- source=data/raw/intro-python-programming.pdf · page=138 · chapter=5 · book_page=128
- auto-check: text_on_page=True, chapter_matches_toc=True
    INFINITE LOOP
    A break statement is an essential part of a loop that does not have a termination condition. A loop without
    a termination condition is known as an infinite loop. Ex: An infinite loop that counts up starting from 1 and
    prints the counter's value while the counter's value is less than 10. A break condition is triggered when the
    counter's value is equal to 10, and hence the program execution exits.
    counter = 1
    while True:
    if counter >= 10:
    break
    print(counter)
    counter += 1

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p141:B:00` score=0.583128
- source=data/raw/intro-python-programming.pdf · page=141 · chapter=5 · book_page=131
- auto-check: text_on_page=True, chapter_matches_toc=True
    statement. A loop else is used to identify if the loop is terminated normally or the execution is interrupted by
    a break statement.
    Ex: A for loop that iterates over a list of numbers to find if the value 10 is in the list. In each iteration, if 10 is
    observed, the statement "Found 10!" is printed and the execution can terminate using a break statement. If
    10 is not in the list, the loop terminates when all integers in the list are evaluated, and hence the else
    statement will run and print "10 is not in the list." Alternatively, a Boolean variable can be used to
    track whether number 10 is found after loop's execution terminates.

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p143:B:02` score=0.546817
- source=data/raw/intro-python-programming.pdf · page=143 · chapter=5 · book_page=133
- auto-check: text_on_page=True, chapter_matches_toc=True
    • A loop else statement runs after the loop's execution is completed without being interrupted by a break
    statement.
    At this point, you should be able to write programs with loop constructs. The programming practice below ties
    together most topics presented in the chapter.
    Function Description
    range(end) Generates a sequence beginning at 0 until end with step size of 1.
    range(start, end) Generates a sequence beginning at start until end with step size of 1.
    range(start, end, s) Generates a sequence beginning at start until end with the step size of s.
    Table 5.4 Chapter 5 reference.
    TRY IT

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding B·q22 (0/1/2):** 2
**Lý do:** #1 p138:B:00 chứa trọn định nghĩa infinite loop và vai trò của break, kèm ví dụ while True.

---

## B · q23 (metadata_filter) — In what situation is the else clause executed?
- Gold: trang 141 (hoặc [143]); filter yêu cầu: {'chapter': 5}; filter áp dụng: None
- Evidence: "A loop else is used to identify if the loop is terminated normally or the execution is interrupted by a break statement."
- Tự động: Hit@1=False, Evidence Hit@3=False

### #1 `openstax-intro-python:p140:B:02` score=0.657374
- source=data/raw/intro-python-programming.pdf · page=140 · chapter=5 · book_page=130
- auto-check: text_on_page=True, chapter_matches_toc=True
    Loop else
    A loop else statement runs after the loop's execution is completed without being interrupted by a break
    TRY IT
    TRY IT

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p102:B:01` score=0.632815
- source=data/raw/intro-python-programming.pdf · page=102 · chapter=4 · book_page=92
- auto-check: text_on_page=True, chapter_matches_toc=True
    An else statement is used with an if statement and contains a body of statements that is executed when the
    if statement's condition is false. When an if-else statement is executed, one and only one of the branches
    is taken. That is, the body of the if or the body of the else is executed. Note: The else statement is at the
    same level of indentation as the if statement, and the body is indented.
    if-else statement template:
    1 # Statements before
    2
    3 if condition:
    4 # Body
    5 else:
    6 # Body
    7
    8 # Statements after

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p123:B:00` score=0.525191
- source=data/raw/intro-python-programming.pdf · page=123 · chapter=4 · book_page=113
- auto-check: text_on_page=True, chapter_matches_toc=True
    Function Description
    elif statement
    # Statements before
    if condition:
    # Body
    elif condition:
    # Body
    else:
    # Body
    # Statements after
    Nested if
    statement
    # Statements before
    if condition:
    if condition:
    # Body
    else:
    # Body
    else:
    if condition:
    # Body
    else:
    # Body
    # Statements after
    Conditional
    expression
    expression_if_true if condition else expression_if_false
    Table 4.5 Chapter 4 reference.

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding B·q23 (0/1/2):** 2
**Lý do:** #1 p140:B:02 nêu 'A loop else statement runs after the loop's execution is completed without being interrupted by a break' (thiếu chữ 'statement' do sang trang) — bằng chứng tương đương, người chấm xác nhận. Nhưng #2, #3 là if-else chương 4 (vi phạm filter). Auto Evidence Hit@3 = False chỉ vì p140 không nằm trong danh sách gold.

---

## B · q24 (exception) — A function normally treats a variable it edits as local. How can it modify a global variable instead?
- Gold: trang 157; filter yêu cầu: None; filter áp dụng: None
- Evidence: "To edit a global variable inside a function, the variable must be declared with the global keyword."
- Tự động: Hit@1=True, Evidence Hit@3=True

### #1 `openstax-intro-python:p157:B:01` score=0.728637
- source=data/raw/intro-python-programming.pdf · page=157 · chapter=6 · book_page=147
- auto-check: text_on_page=True, chapter_matches_toc=True
    Using local and global variables together
    Python allows global and local variables to have the same name, which can lead to unexpected program
    behavior. A function treats a variable edited within the function as a local variable unless told otherwise. To edit
    a global variable inside a function, the variable must be declared with the global keyword.

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p157:B:02` score=0.664044
- source=data/raw/intro-python-programming.pdf · page=157 · chapter=6 · book_page=147
- auto-check: text_on_page=True, chapter_matches_toc=True
    CHECKPOINT
    Editing global variables in a program with a function
    Editing global variables in a program with a function; ch 6, video 8 (https://www.openstax.org/r/editing-
    global-variables)

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p160:B:03` score=0.56536
- source=data/raw/intro-python-programming.pdf · page=160 · chapter=6 · book_page=150
- auto-check: text_on_page=True, chapter_matches_toc=True
    CHECKPOINT
    Global and local variables in a program with a function
    More global and local variables in a program with a function; ch 6, video 9 (https://www.openstax.org/r/
    more-global-and-local-variables)

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding B·q24 (0/1/2):** 2
**Lý do:** #1 p157:B:01 chứa trọn quy tắc dùng từ khóa global, tự đủ ngữ cảnh.

---

## B · q25 (exception) — Why should a list not be used as a default parameter value?
- Gold: trang 170; filter yêu cầu: None; filter áp dụng: None
- Evidence: "Note: Default parameter values are only defined once to be used by the function, so mutable objects (such as lists) should not be used as default values."
- Tự động: Hit@1=False, Evidence Hit@3=True

### #1 `openstax-intro-python:p160:B:02` score=0.431546
- source=data/raw/intro-python-programming.pdf · page=160 · chapter=6 · book_page=150
- auto-check: text_on_page=True, chapter_matches_toc=True
    Arguments and parameters
    What if a programmer wants to write a function that prints the contents of a list? Good practice is to pass
    values directly to a function rather than relying on global variables. A function argument is a value passed as
    input during a function call. A function parameter is a variable representing the input in the function
    definition. Note: The terms "argument" and "parameter" are sometimes used interchangeably in conversation
    and documentation.

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p170:B:02` score=0.413459
- source=data/raw/intro-python-programming.pdf · page=170 · chapter=6 · book_page=160
- auto-check: text_on_page=True, chapter_matches_toc=True
    CHECKPOINT
    Using default parameter values
    Using default parameter values; ch 6, video 14 (https://www.openstax.org/r/default-parameter-values)

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p170:B:01` score=0.349835
- source=data/raw/intro-python-programming.pdf · page=170 · chapter=6 · book_page=160
- auto-check: text_on_page=True, chapter_matches_toc=True
    Default parameter values
    Functions can define default parameter values to use if a positional or keyword argument is not provided for
    the parameter. Ex: def season(m, d, hemi="N"): defines a default value of "N" for the hemi parameter.
    Note: Default parameter values are only defined once to be used by the function, so mutable objects (such as
    lists) should not be used as default values.
    The physics example below calculates weight as a force in newtons given mass in kilograms and acceleration
    in . Gravity on Earth is 9.8 , and gravity on Mars is 3.7 .

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding B·q25 (0/1/2):** 2
**Lý do:** #3 p170:B:01 chứa trọn 'Default parameter values are only defined once..., so mutable objects (such as lists) should not be used'. #1 p160, #2 (link video) là nhiễu.

---

## B · q26 (metadata_filter) — Should there be spaces around the equals sign according to PEP 8?
- Gold: trang 171; filter yêu cầu: {'chapter': 6}; filter áp dụng: None
- Evidence: "The PEP 8 style guide recommends no spaces around = when indicating keyword arguments and default parameter values."
- Tự động: Hit@1=False, Evidence Hit@3=True

### #1 `openstax-intro-python:p110:B:03` score=0.624626
- source=data/raw/intro-python-programming.pdf · page=110 · chapter=4 · book_page=100
- auto-check: text_on_page=True, chapter_matches_toc=True
    PEP 8 RECOMMENDATIONS: SPACING AROUND OPERATORS
    The PEP 8 style guide recommends consistent spacing around operators to avoid extraneous and confusing
    whitespace.
    • Avoid multiple spaces and an unequal amount of whitespace around operators with two operands.
    Avoid: x= y * 44
    Better: x = y * 44
    • Avoid spaces immediately inside parentheses.
    Avoid: x = ( 4 * y )
    Better: x = (4 * y)
    • Surround the following operators with one space: assignment, augment assignment, comparison,

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p171:B:00` score=0.45485
- source=data/raw/intro-python-programming.pdf · page=171 · chapter=6 · book_page=161
- auto-check: text_on_page=True, chapter_matches_toc=True
    PEP 8 RECOMMENDATIONS: SPACING
    The PEP 8 style guide recommends no spaces around = when indicating keyword arguments and default
    parameter values.
    Stream donations
    Write a function, donate(), that lets an online viewer send a donation to a streamer. donate() has three
    parameters:
    • amount: amount to donate, default value: 5
    • name: donor's name, default value: "Anonymous"
    • msg: donor's message, default value: ""
    Given:
    donate(10, "gg")
    The output is:
    Anonymous donated 10 credits: gg
    Write function calls that use the default values along with positional and keyword arguments.
    Access multimedia content (http://openstax.org/books/introduction-python-programming/pages/
    6-6-keyword-arguments)

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p111:B:00` score=0.376329
- source=data/raw/intro-python-programming.pdf · page=111 · chapter=4 · book_page=101
- auto-check: text_on_page=True, chapter_matches_toc=True
    Boolean.
    Avoid: x= y<44
    Better: x = y < 44
    • Consider adding whitespace around operators with lower priority.
    Avoid: x = 5 * z+20
    Better: x = 5*z + 20

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding B·q26 (0/1/2):** 1
**Lý do:** #2 p171 có đáp án đúng, nhưng #1 p110 chương 4 (bao quanh phép gán bằng một dấu cách) xếp trên — mâu thuẫn nếu không biết chương.

---

## C · q21 (paraphrase) — How does Python show that one decision statement is placed inside another?
- Gold: trang 116; filter yêu cầu: None; filter áp dụng: None
- Evidence: "Nesting allows a decision statement to be inside another decision statement, and is indicated by an indentation level."
- Tự động: Hit@1=False, Evidence Hit@3=False

### #1 `openstax-intro-python:p095:B:01` score=0.519051
- source=data/raw/intro-python-programming.pdf · page=95 · chapter=4 · book_page=None
- auto-check: text_on_page=True, chapter_matches_toc=True
    Introduction
    The Python interpreter follows a single path of execution when executing a program. What if a programmer
    wants to define multiple possible paths? Ex: Instead of always taking the left path, a program uses the path
    width to decide which path to take. If the left path is wider, take the right path. Else, take the left path.
    A branch is a group of statements that execute based on a condition. The Expressions chapter introduced
    expressions. This chapter explores how expressions can be used as conditions to make decisions in programs.

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p111:B:02` score=0.496923
- source=data/raw/intro-python-programming.pdf · page=111 · chapter=4 · book_page=101
- auto-check: text_on_page=True, chapter_matches_toc=True
    Two separate if statements do not guarantee that only one branch is taken and might result in both branches
    being taken. Ex: The program below attempts to add a curve based on the input test score. If the input is 60,
    both if statements are incorrectly executed, and the resulting score is 75.
    score = int(input())
    if score < 70:
    score += 10
    # Wrong:
    if 70 <= score < 85:
    score += 5
    Chaining decision statements with elif allows the programmer to check for multiple conditions. An elif (short
    for else if) statement checks a condition when the prior decision statement's condition is false. An elif
    statement is part of a chain and must follow an if (or elif) statement.
    if-elif statement template:
    # Statements before
    if condition:
    # Body
    elif condition:
    # Body
    # Statements after

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p100:B:02` score=0.484264
- source=data/raw/intro-python-programming.pdf · page=100 · chapter=4 · book_page=90
- auto-check: text_on_page=True, chapter_matches_toc=True
    A condition is an expression that evaluates to true or false. An if statement is a decision-making structure
    that contains a condition and a body of statements. If the condition is true, the body is executed. If the
    condition is false, the body is not executed.
    The if statement's body must be grouped together and have one level of indentation. The PEP 8 style guide
    recommends four spaces per indentation level. The Python interpreter will produce an error if the body is
    empty.
    TRY IT
    TRY IT

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding C·q21 (0/1/2):** 1
**Lý do:** Giống B (câu không có filter, cùng top-3): chỉ có bằng chứng gián tiếp ở p100 về thụt lề thân if.

---

## C · q22 (direct) — What is a loop with no termination condition called, and what statement lets it stop?
- Gold: trang 138; filter yêu cầu: None; filter áp dụng: None
- Evidence: "A break statement is an essential part of a loop that does not have a termination condition. A loop without a termination condition is known as an infinite loop."
- Tự động: Hit@1=True, Evidence Hit@3=True

### #1 `openstax-intro-python:p138:B:00` score=0.59176
- source=data/raw/intro-python-programming.pdf · page=138 · chapter=5 · book_page=128
- auto-check: text_on_page=True, chapter_matches_toc=True
    INFINITE LOOP
    A break statement is an essential part of a loop that does not have a termination condition. A loop without
    a termination condition is known as an infinite loop. Ex: An infinite loop that counts up starting from 1 and
    prints the counter's value while the counter's value is less than 10. A break condition is triggered when the
    counter's value is equal to 10, and hence the program execution exits.
    counter = 1
    while True:
    if counter >= 10:
    break
    print(counter)
    counter += 1

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p141:B:00` score=0.583128
- source=data/raw/intro-python-programming.pdf · page=141 · chapter=5 · book_page=131
- auto-check: text_on_page=True, chapter_matches_toc=True
    statement. A loop else is used to identify if the loop is terminated normally or the execution is interrupted by
    a break statement.
    Ex: A for loop that iterates over a list of numbers to find if the value 10 is in the list. In each iteration, if 10 is
    observed, the statement "Found 10!" is printed and the execution can terminate using a break statement. If
    10 is not in the list, the loop terminates when all integers in the list are evaluated, and hence the else
    statement will run and print "10 is not in the list." Alternatively, a Boolean variable can be used to
    track whether number 10 is found after loop's execution terminates.

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p143:B:02` score=0.546817
- source=data/raw/intro-python-programming.pdf · page=143 · chapter=5 · book_page=133
- auto-check: text_on_page=True, chapter_matches_toc=True
    • A loop else statement runs after the loop's execution is completed without being interrupted by a break
    statement.
    At this point, you should be able to write programs with loop constructs. The programming practice below ties
    together most topics presented in the chapter.
    Function Description
    range(end) Generates a sequence beginning at 0 until end with step size of 1.
    range(start, end) Generates a sequence beginning at start until end with step size of 1.
    range(start, end, s) Generates a sequence beginning at start until end with the step size of s.
    Table 5.4 Chapter 5 reference.
    TRY IT

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding C·q22 (0/1/2):** 2
**Lý do:** Giống B: #1 p138 đủ để trả lời và truy nguồn.

---

## C · q23 (metadata_filter) — In what situation is the else clause executed?
- Gold: trang 141 (hoặc [143]); filter yêu cầu: {'chapter': 5}; filter áp dụng: {'chapter': 5}
- Evidence: "A loop else is used to identify if the loop is terminated normally or the execution is interrupted by a break statement."
- Tự động: Hit@1=False, Evidence Hit@3=True

### #1 `openstax-intro-python:p140:B:02` score=0.657374
- source=data/raw/intro-python-programming.pdf · page=140 · chapter=5 · book_page=130
- auto-check: text_on_page=True, chapter_matches_toc=True
    Loop else
    A loop else statement runs after the loop's execution is completed without being interrupted by a break
    TRY IT
    TRY IT

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p140:B:01` score=0.511162
- source=data/raw/intro-python-programming.pdf · page=140 · chapter=5 · book_page=130
- auto-check: text_on_page=True, chapter_matches_toc=True
    5.5 Loop else
    Learning objectives
    By the end of this section you should be able to
    • Use loop else statement to identify when the loop execution is interrupted using a break statement.
    • Implement a loop else statement with a for or a while loop.

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p141:B:00` score=0.505994
- source=data/raw/intro-python-programming.pdf · page=141 · chapter=5 · book_page=131
- auto-check: text_on_page=True, chapter_matches_toc=True
    statement. A loop else is used to identify if the loop is terminated normally or the execution is interrupted by
    a break statement.
    Ex: A for loop that iterates over a list of numbers to find if the value 10 is in the list. In each iteration, if 10 is
    observed, the statement "Found 10!" is printed and the execution can terminate using a break statement. If
    10 is not in the list, the loop terminates when all integers in the list are evaluated, and hence the else
    statement will run and print "10 is not in the list." Alternatively, a Boolean variable can be used to
    track whether number 10 is found after loop's execution terminates.

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding C·q23 (0/1/2):** 2
**Lý do:** #1 p140 (định nghĩa loop else), #3 p141 chứa evidence gold. Cả 3 chunk thuộc chương 5, không còn nhiễu if-else.

---

## C · q24 (exception) — A function normally treats a variable it edits as local. How can it modify a global variable instead?
- Gold: trang 157; filter yêu cầu: None; filter áp dụng: None
- Evidence: "To edit a global variable inside a function, the variable must be declared with the global keyword."
- Tự động: Hit@1=True, Evidence Hit@3=True

### #1 `openstax-intro-python:p157:B:01` score=0.728637
- source=data/raw/intro-python-programming.pdf · page=157 · chapter=6 · book_page=147
- auto-check: text_on_page=True, chapter_matches_toc=True
    Using local and global variables together
    Python allows global and local variables to have the same name, which can lead to unexpected program
    behavior. A function treats a variable edited within the function as a local variable unless told otherwise. To edit
    a global variable inside a function, the variable must be declared with the global keyword.

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p157:B:02` score=0.664044
- source=data/raw/intro-python-programming.pdf · page=157 · chapter=6 · book_page=147
- auto-check: text_on_page=True, chapter_matches_toc=True
    CHECKPOINT
    Editing global variables in a program with a function
    Editing global variables in a program with a function; ch 6, video 8 (https://www.openstax.org/r/editing-
    global-variables)

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p160:B:03` score=0.56536
- source=data/raw/intro-python-programming.pdf · page=160 · chapter=6 · book_page=150
- auto-check: text_on_page=True, chapter_matches_toc=True
    CHECKPOINT
    Global and local variables in a program with a function
    More global and local variables in a program with a function; ch 6, video 9 (https://www.openstax.org/r/
    more-global-and-local-variables)

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding C·q24 (0/1/2):** 2
**Lý do:** Giống B: #1 p157 đủ để trả lời.

---

## C · q25 (exception) — Why should a list not be used as a default parameter value?
- Gold: trang 170; filter yêu cầu: None; filter áp dụng: None
- Evidence: "Note: Default parameter values are only defined once to be used by the function, so mutable objects (such as lists) should not be used as default values."
- Tự động: Hit@1=False, Evidence Hit@3=True

### #1 `openstax-intro-python:p160:B:02` score=0.431546
- source=data/raw/intro-python-programming.pdf · page=160 · chapter=6 · book_page=150
- auto-check: text_on_page=True, chapter_matches_toc=True
    Arguments and parameters
    What if a programmer wants to write a function that prints the contents of a list? Good practice is to pass
    values directly to a function rather than relying on global variables. A function argument is a value passed as
    input during a function call. A function parameter is a variable representing the input in the function
    definition. Note: The terms "argument" and "parameter" are sometimes used interchangeably in conversation
    and documentation.

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p170:B:02` score=0.413459
- source=data/raw/intro-python-programming.pdf · page=170 · chapter=6 · book_page=160
- auto-check: text_on_page=True, chapter_matches_toc=True
    CHECKPOINT
    Using default parameter values
    Using default parameter values; ch 6, video 14 (https://www.openstax.org/r/default-parameter-values)

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p170:B:01` score=0.349835
- source=data/raw/intro-python-programming.pdf · page=170 · chapter=6 · book_page=160
- auto-check: text_on_page=True, chapter_matches_toc=True
    Default parameter values
    Functions can define default parameter values to use if a positional or keyword argument is not provided for
    the parameter. Ex: def season(m, d, hemi="N"): defines a default value of "N" for the hemi parameter.
    Note: Default parameter values are only defined once to be used by the function, so mutable objects (such as
    lists) should not be used as default values.
    The physics example below calculates weight as a force in newtons given mass in kilograms and acceleration
    in . Gravity on Earth is 9.8 , and gravity on Mars is 3.7 .

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding C·q25 (0/1/2):** 2
**Lý do:** Giống B (câu không có filter): #3 p170 đủ lý do và kết luận.

---

## C · q26 (metadata_filter) — Should there be spaces around the equals sign according to PEP 8?
- Gold: trang 171; filter yêu cầu: {'chapter': 6}; filter áp dụng: {'chapter': 6}
- Evidence: "The PEP 8 style guide recommends no spaces around = when indicating keyword arguments and default parameter values."
- Tự động: Hit@1=True, Evidence Hit@3=True

### #1 `openstax-intro-python:p171:B:00` score=0.45485
- source=data/raw/intro-python-programming.pdf · page=171 · chapter=6 · book_page=161
- auto-check: text_on_page=True, chapter_matches_toc=True
    PEP 8 RECOMMENDATIONS: SPACING
    The PEP 8 style guide recommends no spaces around = when indicating keyword arguments and default
    parameter values.
    Stream donations
    Write a function, donate(), that lets an online viewer send a donation to a streamer. donate() has three
    parameters:
    • amount: amount to donate, default value: 5
    • name: donor's name, default value: "Anonymous"
    • msg: donor's message, default value: ""
    Given:
    donate(10, "gg")
    The output is:
    Anonymous donated 10 credits: gg
    Write function calls that use the default values along with positional and keyword arguments.
    Access multimedia content (http://openstax.org/books/introduction-python-programming/pages/
    6-6-keyword-arguments)

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #2 `openstax-intro-python:p152:B:00` score=0.306497
- source=data/raw/intro-python-programming.pdf · page=152 · chapter=6 · book_page=142
- auto-check: text_on_page=True, chapter_matches_toc=True
    CONCEPTS IN PRACTICE
    Following the control flow
    1 . Which line is executed first?
    1 def park_greet():
    2 """Output greeting."""
    3 print("Welcome. Open sunrise to sunset.")
    4
    5 car_count = 1
    6 park_greet()
    7 if car_count > 50:
    8 # Direct to extra parking lot
    a. 1
    b. 3
    c. 5
    2 . Control flow moves to line 9, and park_greet() is called. Which line does control flow move to next?
    1 def extra_lot():
    2 # Function definition
    3
    4 def park_greet():
    5 """Output greeting."""
    6 print("Welcome. Open sunrise to sunset.")
    7
    8 car_count = 1
    9 park_greet()
    10 if car_count > 50:
    11 extra_lot()
    a. 1
    b. 4
    c. 10
    3 . Control flow moves to line 12, and extra_lot() is called. Which line does control flow move to after
    line 3 is executed?
    1 def extra_lot():

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

### #3 `openstax-intro-python:p160:B:04` score=0.287839
- source=data/raw/intro-python-programming.pdf · page=160 · chapter=6 · book_page=150
- auto-check: text_on_page=True, chapter_matches_toc=True
    CONCEPTS IN PRACTICE
    Arguments and parameters
    Consider the following:
    1 def print_welcome(name):
    2 print(f"Welcome {name}!")
    3
    4 username = int(input("Enter new username: "))
    5 print_welcome(username)

- Metadata đủ và đúng (có/không, lỗi): có — source, page, chapter khớp PDF

**Grounding C·q26 (0/1/2):** 2
**Lý do:** #1 p171:B:00 có đáp án đúng; filter chapter=6 loại các đoạn PEP 8 của chương 4. #2, #3 cùng chương, không mâu thuẫn.

---

## Tổng hợp (đã duyệt)

| Strategy | Grounding 0 / 1 / 2 (số câu) | Trung bình /2 | Metadata đủ và đúng | Filter tuân thủ (test) |
|---|---|---:|---|---|
| A | 2 / 2 / 2 | 1.00 | 18/18 | 0/2 |
| B | 0 / 2 / 4 | 1.67 | 18/18 | 0/2 |
| C | 0 / 1 / 5 | 1.83 | 18/18 | 2/2 |

- Metadata: đã kiểm từng bản ghi top-3 (6 câu × 3) — text chunk nằm đúng ở `page` ghi trong metadata, `chapter` khớp mục lục, `source` trỏ đúng file PDF (đường dẫn local; URL gốc nằm trong manifest). Không phát hiện lỗi. Hạn chế: `book_page` rỗng ở trang mở chương (95, 125, 147) vì trang đó không có footer chuẩn; chưa có trường `section`.
- Bằng chứng tương đương do người chấm xác nhận (không đổi gold, không đổi chỉ số tự động): **B·q23 #1 p140**. Nếu tính, Evidence Hit@3 test của B sẽ là 5/6 thay vì 4/6 (Hit@1 3/6 thay vì 2/6); C·q23 #1 cũng là p140 → Hit@1 test của C sẽ là 4/6.
