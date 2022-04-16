# task1
# nhập tên của một tệp và truy cập đọc
import re

fname = input("Enter a class file to grade (i.e. class1 for class1.txt): ")
try:
    with open(fname) as data:
        fh = data.readlines()
    print('Successfully opened', fname)
except:
    print('File cannot be found.')
    exit()
# task2
print('*** ANALYZING ***')
true_line = 0
false_line = 0
for line in fh:
    # scan với điều kiện: Một dòng không hợp lệ chứa danh sách khác 26 giá trị được phân tách bằng dấu phẩy
    line = line.rstrip()
    values = line.split(',')
    if len(values) != 26:
        false_line = false_line + 1
        print('Invalid line of data: does not contain exactly 26 values:\n', line)
        continue
    # scan với điều kiện:1 dòng không hợp lệ không chứa ký tự “N” theo sau là 8 ký tự số
    elif not (re.search('^N\d{8}', line)):
        false_line = false_line + 1
        print('Invalid line of data: N# is invalid\n', line)
        continue
    # các trường hợp còn lại là dòng hợp lệ
    else:
        true_line = true_line + 1

if false_line == 0:
    print('No errors found!')
print('*** REPORT ***')
print('Total valid lines of data:{}'.format(true_line),
      'Total invalid lines of data:{}'.format(false_line),
      sep='\n')
# task3
answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
ans_key = answer_key.split(',')
so_hs = true_line
high_grade = 0
lst_grade = []
dict_grade = {}
skip_ans = {}
wrong_ans = {}
for line in fh:
    line = line.rstrip()
    values = line.split(',')
    #loại các dòng không đúng pattern
    if len(values) != 26 or not (re.search('^N\d{8}', line)): continue
    #tính điểm đạt được của mỗi học sinh
    grade = 0
    for num in range(len(ans_key)):
        if values[num+1] == ans_key[num]:
            grade = grade + 4
        elif values[num+1] == '':
            skip_ans[num+1] = skip_ans.get(num+1, 0) + 1
        else:
            grade = grade - 1
            wrong_ans[num+1] = wrong_ans.get(num+1, 0) + 1
    #tạo danh sách điểm
    lst_grade.append(grade)
    lst_grade.sort()
    #tạo từ điển với key = mã học sinh, value = điểm đạt được
    dict_grade[values[0]] = grade
    #đếm số học sinh điểm >80
    if grade > 80:
        high_grade = high_grade + 1
tb_grade = round(sum(lst_grade) / so_hs, 3)
#tìm miền giá trị của điểm
best = 0
worst = 101
for i in range(len(lst_grade)):
    if lst_grade[i] > best:
        best = lst_grade[i]
    if lst_grade[i] < worst:
        worst = lst_grade[i]
range_grade = best - worst
#tìm trung vị
if so_hs % 2 == 0:
    trung_vi = (lst_grade[round(len(lst_grade) / 2 - 1)] + lst_grade[round(len(lst_grade) / 2)]) / 2
else:
    trung_vi = lst_grade[round(so_hs / 2)]
#khai báo biến
num_skip = 0
num_wrong = 0
skip_lst = []
wrong_lst = []
#tìm câu hỏi bị học sinh bỏ qua nhiều nhất
for qst, num in skip_ans.items():
    if num > num_skip:
        num_skip = num
#tỉ lệ bị bỏ qua
skip_rate = round(num_skip / so_hs, 3)
#tạo list với cấu trúc:số thứ tự câu hỏi - số lượng học sinh bỏ qua -  tỉ lệ bị bỏ qua
for qst, num in skip_ans.items():
    if num == num_skip:
        x = ' - '.join([str(qst), str(num), str(skip_rate)])
        skip_lst.append(x)
str_skip = ', '.join(skip_lst)
#tìm câu hỏi bị học sinh sai qua nhiều nhất
for qst, num in wrong_ans.items():
    if num > num_wrong:
        num_wrong = num
#tỉ lệ bị sai
wrong_rate = round(num_wrong / so_hs, 3)
#tạo list với cấu trúc: số thứ tự câu hỏi - số lượng học sinh trả lời sai - tỉ lệ bị sai
for qst, num in wrong_ans.items():
    if num == num_wrong:
        y = ' - '.join([str(qst), str(num), str(wrong_rate)])
        wrong_lst.append(y)
str_wrong = ', '.join(wrong_lst)
#in ra các kết quả đã tính
print('Total student of high scores: {}'.format(high_grade),
      'Mean (average) score: {}'.format(tb_grade),
      'Highest score: {}'.format(best),
      'Lowest score: {}'.format(worst),
      'Range of scores: {}'.format(range_grade),
      'Median score: {}\n'.format(trung_vi),
      'Question that most people skip: {}\n'.format(str_skip),
      'Question that most people answer incorrectly: {}'.format(str_wrong),
      sep = '\n'
      )
#task4
name = (fname.split('.'))[0]
with open(name+'_grades.txt', 'w') as fw:
    for msv, score in dict_grade.items():
        fw.write('{},{}\n'.format(msv, score))
