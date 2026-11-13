# Coherence audit — 10 vị trí chốt trước (giữa trang)

Thang: 0 = cắt giữa ý / thiếu chủ thể; 1 = hiểu một phần, thiếu ngữ cảnh; 2 = tự hiểu, giữ trọn ý.
C dùng chung chunk với B nên điểm coherence của C = B.

Người chấm: Trần Văn Tài (tác giả bài) — chấm thủ công, có biết kết quả Hit@k trước khi chấm nên có nguy cơ thiên lệch. Nguyên tắc: chấm ý tại đúng vị trí đã chọn; nội dung thừa ở đầu/cuối chunk chỉ trừ điểm khi làm ý tại vị trí bị cắt hoặc thiếu ngữ cảnh.

## Trang PDF 95 — vị trí ký tự 606
Ngữ cảnh nguồn quanh vị trí: `…e. If the left path is wider, take the right path. Else, take the left path. / A branch is a group of statements that exec…`

### A: `openstax-intro-python:p095:A:01` [450:950]
    nstead of always taking the left path, a program uses the path
    width to decide which path to take. If the left path is wider, take the right path. Else, take the left path.
    A branch is a group of statements that execute based on a condition. The Expressions chapter introduced
    expressions. This chapter explores how expressions can be used as conditions to make decisions in programs.
    4.1 Boolean values
    Learning objectives
    By the end of this section you should be able to
    • Explain a Boolean value.
    

- Điểm A: 1
- Lý do A: Có phần giải thích về nhánh điều kiện, nhưng chunk bị cắt giữa từ ở đầu và chuyển sang mục tiêu học tập chưa trọn ở cuối.

### B: `openstax-intro-python:p095:B:01` [286:834]
    Introduction
    The Python interpreter follows a single path of execution when executing a program. What if a programmer
    wants to define multiple possible paths? Ex: Instead of always taking the left path, a program uses the path
    width to decide which path to take. If the left path is wider, take the right path. Else, take the left path.
    A branch is a group of statements that execute based on a condition. The Expressions chapter introduced
    expressions. This chapter explores how expressions can be used as conditions to make decisions in programs.

- Điểm B: 2
- Lý do B: Giữ trọn phần giới thiệu về nhánh và vai trò của biểu thức điều kiện.

## Trang PDF 103 — vị trí ký tự 390
Ngữ cảnh nguồn quanh vị trí: `…ion / The following program divides two integers. Division by 0 produces an error. Modify the program to read in / a new den…`

### A: `openstax-intro-python:p103:A:00` [0:500]
    if x >= 15:
    # Do something
    else:
    # Do something else
    a. x >= 15
    b. x <= 15
    c. x < 15
    7 . Given x = 40, what is the final value of y?
    if x > 30:
    y = x - 10
    else:
    y = x + 10
    a. 30
    b. 40
    c. 50
    8 . Given y = 50, which is not a possible final value of y?
    if x < 50:
    y = y / 2
    else:
    y = y * 2
    y = y + 5
    a. 30
    b. 55
    c. 105
    Improved division
    The following program divides two integers. Division by 0 produces an error. Modify the program to read in
    a new denominator (with no prompt) if the denominator is 0.

- Điểm A: 2
- Lý do A: Nêu rõ vấn đề chia cho 0 và yêu cầu đọc lại mẫu số; nội dung bài tập hiểu được độc lập.

### B: `openstax-intro-python:p103:B:01` [316:616]
    Improved division
    The following program divides two integers. Division by 0 produces an error. Modify the program to read in
    a new denominator (with no prompt) if the denominator is 0.
    Access multimedia content (http://openstax.org/books/introduction-python-programming/pages/4-2-if-
    else-statements)

- Điểm B: 2
- Lý do B: Mô tả đầy đủ yêu cầu bài tập và điều kiện cần xử lý.

## Trang PDF 111 — vị trí ký tự 745
Ngữ cảnh nguồn quanh vị trí: `…ible missed connection. / Two separate if statements do not guarantee that only one branch is taken and might result in bo…`

### A: `openstax-intro-python:p111:A:01` [450:950]
    ngle condition. Ex: A travel planning site reviews
    the layovers on an itinerary. If a layover is greater than 24 hours, the site should suggest accommodations.
    Else if the layover is less than one hour, the site should alert for a possible missed connection.
    Two separate if statements do not guarantee that only one branch is taken and might result in both branches
    being taken. Ex: The program below attempts to add a curve based on the input test score. If the input is 60,
    both if statements are 

- Điểm A: 1
- Lý do A: Ý chính về hai câu lệnh if đã có, nhưng phần ví dụ bị cắt giữa câu ở cuối chunk.

### B: `openstax-intro-python:p111:B:02` [709:1490]
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

- Điểm B: 2
- Lý do B: Giải thích trọn vấn đề của hai câu lệnh if và cách chuỗi elif xử lý nhiều điều kiện.

## Trang PDF 119 — vị trí ký tự 714
Ngữ cảnh nguồn quanh vị trí: `… by first checking the condition. If condition is true, / expression_if_true is evaluated, and the result is the resulting…`

### A: `openstax-intro-python:p119:A:01` [450:950]
    ary operator") is a simplified, single-line version of an
    if-else statement.
    Conditional expression template:
    expression_if_true if condition else expression_if_false
    A conditional expression is evaluated by first checking the condition. If condition is true,
    expression_if_true is evaluated, and the result is the resulting value of the conditional expression. Else,
    expression_if_false is evaluated, and the result is the resulting value of the conditional expression.
    A variable can be assigned wi

- Điểm A: 1
- Lý do A: Có mẫu và giải thích conditional expression, nhưng bị cắt từ ở đầu và kết thúc giữa câu về phép gán.

### B: `openstax-intro-python:p119:B:02` [379:1147]
    Conditional expressions
    A conditional expression (also known as a "ternary operator") is a simplified, single-line version of an
    if-else statement.
    Conditional expression template:
    expression_if_true if condition else expression_if_false
    A conditional expression is evaluated by first checking the condition. If condition is true,
    expression_if_true is evaluated, and the result is the resulting value of the conditional expression. Else,
    expression_if_false is evaluated, and the result is the resulting value of the conditional expression.
    A variable can be assigned with a conditional expression. Ex: Finding the max of two numbers can be
    calculated with max_num = y if x < y else x
    Note: Conditional expressions have the lowest precedence of all Python operations.

- Điểm B: 2
- Lý do B: Định nghĩa, cú pháp và ví dụ được trình bày đầy đủ, tự hiểu được.

## Trang PDF 128 — vị trí ký tự 681
Ngữ cảnh nguồn quanh vị trí: `…ceived, print "The while loop condition has been met.". / Enter different input words to see when the while loop condition…`

### A: `openstax-intro-python:p128:A:01` [450:950]
    until the user enters "begin". Test the code with
    the given input values to check that the loop does not terminate until the input is "begin". Once the input
    "begin" is received, print "The while loop condition has been met.".
    Enter different input words to see when the while loop condition is met.
    Access multimedia content (http://openstax.org/books/introduction-python-programming/pages/5-1-while-
    loop)
    Sum of odd numbers
    Write a program that reads two integer values, n1 and n2. Use a while loo

- Điểm A: 1
- Lý do A: Nội dung bài tập chính vẫn hiểu được nhưng chunk bắt đầu giữa câu hướng dẫn và có phần chuyển sang bài kế tiếp.

### B: `openstax-intro-python:p128:B:00` [0:749]
    a. value of n after the loop is -1.
    b. value of n after the loop is 0.
    c. value of n after the loop is 1.
    6 . What happens if the code is changed as follows?
    n = 4
    while n > 0:
    print(n)
    # Modified line
    n = n + 1
    print("value of n after the loop is", n)
    a. The code will not run.
    b. The code will run for one additional iteration.
    c. The code will never terminate.
    Reading inputs in a while loop
    Write a program that takes user inputs in a while loop until the user enters "begin". Test the code with
    the given input values to check that the loop does not terminate until the input is "begin". Once the input
    "begin" is received, print "The while loop condition has been met.".
    Enter different input words to see when the while loop condition is met.

- Điểm B: 2
- Lý do B: Bài tập while loop có mục tiêu và hướng dẫn đầy đủ, đủ ngữ cảnh để hiểu độc lập.

## Trang PDF 136 — vị trí ký tự 440
Ngữ cảnh nguồn quanh vị trí: `…the inner loop iterates over all even numbers less than a given number from the / list using a while loop. / numbers = [12, …`

### A: `openstax-intro-python:p136:A:00` [0:500]
    b. for i in range(1, 4):
    for j in range(4):
    print(i * j)
    c. for i in range(1, 4):
    for j in range(4):
    print(i * j, end = ' ')
    print()
    MIXED LOOPS
    The two for and while loop constructs can also be mixed in a nested loop construct. Ex: Printing even
    numbers less than a given number in a list. The outer loop can be implemented using a for loop iterating
    over the provided list, and the inner loop iterates over all even numbers less than a given number from the
    list using a while loop.
    numbers = [12, 

- Điểm A: 1
- Lý do A: Có phần giải thích mixed loops nhưng lẫn nội dung bài trước và ví dụ code bị cắt.

### B: `openstax-intro-python:p136:B:01` [133:665]
    MIXED LOOPS
    The two for and while loop constructs can also be mixed in a nested loop construct. Ex: Printing even
    numbers less than a given number in a list. The outer loop can be implemented using a for loop iterating
    over the provided list, and the inner loop iterates over all even numbers less than a given number from the
    list using a while loop.
    numbers = [12, 5, 3]
    i = 0
    for n in numbers:
    while i < n:
    print (i, end = " ")
    i += 2
    i = 0
    print()
    Printing a triangle of numbers
    Write a program that prints the following output:

- Điểm B: 2
- Lý do B: Giải thích đầy đủ vai trò vòng lặp ngoài/trong và minh họa bằng code.

## Trang PDF 144 — vị trí ký tự 288
Ngữ cảnh nguồn quanh vị trí: `…loop / Nested while loop / while outer_loop_expression: / # outer loop body (1) / while inner_loop_expression: / # inner loop body…`

### A: `openstax-intro-python:p144:A:00` [0:500]
    Function Description
    Loop constructs Description
    while loop
    # initialization
    while expression:
    # loop body
    # statements after the loop
    for loop
    # initialization
    for loop_variable in container:
    # loop body
    # statements after the loop
    Nested while loop
    while outer_loop_expression:
    # outer loop body (1)
    while inner_loop_expression:
    # inner loop body
    # outer loop body (2)
    # statements after the loop
    break statement
    # initialization
    while loop_expression:
    # loop body
    if break_condition:
    break
    # remai

- Điểm A: 2
- Lý do A: Mẫu nested while loop đủ các phần chính để hiểu cấu trúc; phần bị cắt thuộc mục kế tiếp.

### B: `openstax-intro-python:p144:B:00` [0:576]
    Function Description
    Loop constructs Description
    while loop
    # initialization
    while expression:
    # loop body
    # statements after the loop
    for loop
    # initialization
    for loop_variable in container:
    # loop body
    # statements after the loop
    Nested while loop
    while outer_loop_expression:
    # outer loop body (1)
    while inner_loop_expression:
    # inner loop body
    # outer loop body (2)
    # statements after the loop
    break statement
    # initialization
    while loop_expression:
    # loop body
    if break_condition:
    break
    # remaining body of loop
    # statements after the loop
    Table 5.4 Chapter 5 reference.

- Điểm B: 2
- Lý do B: Bảng tham khảo có mẫu nested while loop đầy đủ và trọn vẹn.

## Trang PDF 153 — vị trí ký tự 504
Ngữ cảnh nguồn quanh vị trí: `…y call a function that calculates sales tax. When a function called from / another function finishes execution, control fl…`

### A: `openstax-intro-python:p153:A:01` [450:950]
     a function that calculates sales tax. When a function called from
    another function finishes execution, control flow returns to the calling function.
    CHECKPOINT
    Example: Book club email messages
    Example: Book club email messages; ch 6, video 5 (https://www.openstax.org/r/email-messages)
    CONCEPTS IN PRACTICE
    Functions calling functions
    Consider the book club example above.
    5 . How many function calls occur during the execution of the program?
    a. 2
    b. 3
    c. 6
    6 . When line 3 is reached and executed

- Điểm A: 1
- Lý do A: Có định nghĩa về luồng điều khiển khi gọi hàm, nhưng bị lẫn checkpoint và câu hỏi cuối bị cắt.

### B: `openstax-intro-python:p153:B:01` [245:599]
    Welcome to the park
    Functions calling functions
    Functions frequently call other functions to keep the modularity of each function performing one task. Ex: A
    function that calculates an order total may call a function that calculates sales tax. When a function called from
    another function finishes execution, control flow returns to the calling function.

- Điểm B: 2
- Lý do B: Giải thích trọn ý về hàm gọi hàm khác và trả quyền điều khiển về hàm gọi.

## Trang PDF 161 — vị trí ký tự 561
Ngữ cảnh nguồn quanh vị trí: `…st use the correct order and number of arguments to avoid / undesired behavior and errors (unless using optional or keywor…`

### A: `openstax-intro-python:p161:A:01` [450:950]
    ute
    the square footage of a room. Function calls must use the correct order and number of arguments to avoid
    undesired behavior and errors (unless using optional or keyword arguments as discussed later).
    EXAMPLE 6.1
    Using multiple arguments in a function call
    def print_div(op_1, op_2):
    """ Prints division operation """
    print(f"{op_1}/{op_2} = {op_1/op_2}")
    num_1 = 6
    num_2 = 3
    print_div(num_1, num_2) # Prints "6/3 = 2.0"
    print_div(num_2, num_1) # Prints "3/6 = 0.5"
    print_div(num_1) # Error: Missi

- Điểm A: 1
- Lý do A: Quy tắc về số lượng/thứ tự đối số có đủ, nhưng ví dụ code kết thúc giữa dòng lỗi.

### B: `openstax-intro-python:p161:B:01` [315:653]
    Multiple arguments and parameters
    Functions can have multiple parameters. Ex: A function uses two parameters, length and width, to compute
    the square footage of a room. Function calls must use the correct order and number of arguments to avoid
    undesired behavior and errors (unless using optional or keyword arguments as discussed later).

- Điểm B: 2
- Lý do B: Giải thích rõ quan hệ giữa nhiều tham số và đối số, kèm ví dụ ngữ cảnh.

## Trang PDF 169 — vị trí ký tự 677
Ngữ cảnh nguồn quanh vị trí: `…before any keyword arguments. / CHECKPOINT / Using keyword arguments / Using keyword arguments; ch 6, video 13 (https://www.op…`

### A: `openstax-intro-python:p169:A:01` [450:950]
     that use parameter names
    to assign values rather than order. When mixing positional and keyword arguments, positional arguments
    must come first in the correct order, before any keyword arguments.
    CHECKPOINT
    Using keyword arguments
    Using keyword arguments; ch 6, video 13 (https://www.openstax.org/r/keyword-arguments)
    CONCEPTS IN PRACTICE
    Using keyword and positional arguments
    Consider the following function:
    def greeting(msg, name, count):
    i = 0
    for i in range(0, count):
    print(msg, name)
    1 . Whi

- Điểm A: 1
- Lý do A: Quy tắc thứ tự positional/keyword argument có thể hiểu được, nhưng câu hỏi checkpoint phía sau bị cắt.

### B: `openstax-intro-python:p169:B:02` [647:768]
    CHECKPOINT
    Using keyword arguments
    Using keyword arguments; ch 6, video 13 (https://www.openstax.org/r/keyword-arguments)

- Điểm B: 0
- Lý do B: Chỉ có tiêu đề checkpoint và liên kết video, không có phần giải thích nội dung cần đánh giá.

## Tổng hợp

| Strategy | Điểm trung bình (/2) |
|---|---:|
| A | 1.2 |
| B | 1.8 |
| C | 1.8 (dùng chung chunk với B) |
