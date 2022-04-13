
from pororo import Pororo
from dataclasses import dataclass
import copy
from tkinter import *
from tkinter import scrolledtext
import random

# 체크할 유의미한 형태소 dict
word_data = {('빨갛', 'VA'):['red', 'color'], ('붉', 'VA'):['red', 'color'], ('발갛', 'VA'):['red', 'color'], ('새빨갛', 'VA'):['red', 'color'], ('뻘겋', 'VA'):['red', 'color'], ('빨간', 'NNG'):['red', 'color'], ('빨강', 'NNG'):['red', 'color'], ('붉은', 'NNP'):['red', 'color'], ('적색', 'NNG'):['red', 'color'],
             ('파랗', 'VA'):['blue', 'color'], ('푸르', 'VA'):['blue', 'color'], ('퍼렇', 'VA'):['blue', 'color'], ('새파랗', 'VA'):['blue', 'color'], ('시퍼렇', 'VA'):['blue', 'color'], ('파란', 'NNG'):['blue', 'color'], ('파랑', 'NNG'):['blue', 'color'], ('퍼런', 'NNG'):['blue', 'color'], ('청색', 'NNG'):['blue', 'color'], ('청', 'NNG'):['blue', 'color'],
             ('초록', 'NNG'):['green', 'color'], ('녹색', 'NNG'):['green', 'color'],
             ('노랗', 'VA'):['yellow', 'color'], ('누렇', 'VA'):['yellow', 'color'], ('샛노랗', 'VA'):['yellow', 'color'], ('누르', 'VA'):['yellow', 'color'], ('황색', 'NNG'):['yellow', 'color'], ('노란', 'NNG'):['yellow', 'color'], ('노랑', 'NNG'):['yellow', 'color'], ('누런', 'NNG'):['yellow', 'color'],
             ('주황', 'NNG'):['orange', 'color'], ('자황', 'NNG'):['orange', 'color'], ('귤색', 'NNG'):['orange', 'color'], ('감색', 'NNG'):['orange', 'color'],
             ('보라', 'NNG'):['violet', 'color'], ('보랏', 'NNG'):['violet', 'color'], ('자색', 'NNG'):['violet', 'color'], ('자주', 'NNG'):['violet', 'color'], ('자줏', 'NNG'):['violet', 'color'],
             ('하얗', 'VA'):['white', 'color'], ('허옇', 'VA'):['white', 'color'], ('희', 'VA'):['white', 'color'], ('하얀', 'NNG'):['white', 'color'], ('허연', 'NNG'):['white', 'color'], ('흰', 'NNG'):['white', 'color'],
             ('까맣', 'VA'):['black', 'color'], ('새까맣', 'VA'):['black', 'color'], ('새카맣', 'VA'):['black', 'color'], ('검', 'VA'):['black', 'color'], ('검정', 'NNG'):['black', 'color'],
             ('동그라미', 'NNG'):['circle', 'figure'], ('원', 'NNG'):['circle', 'figure'], ('원형', 'NNG'):['circle', 'figure'],
             ('세모', 'NNG'):['tri', 'figure'], ('삼각', 'NNG'):['tri', 'figure'],
             ('사각', 'NNG'):['rect', 'figure'], ('사변', 'NNG'):['rect', 'figure'], ('네', 'NNG'):['rect', 'figure'], ('네모', 'NNG'):['rect', 'figure'],
             ('별', 'NNG'):['star', 'figure'], ('별표', 'NNG'):['star', 'figure'], ('별', 'MM'):['star', 'figure'],
             ('하트', 'NNG'):['heart', 'figure'],
             ('위', 'NNG'):['up', 'position'], ('윗', 'NNG'):['up', 'position'], ('꼭대기', 'NNG'):['up', 'position'], ('상', 'NNG'):['up', 'position'], ('상단', 'NNG'):['up', 'position'], ('상측', 'NNG'):['up', 'position'], ('위', 'NNBC'):['up', 'position'],
             ('아래', 'NNG'):['down', 'position'], ('밑', 'NNG'):['down', 'position'], ('하단', 'NNG'):['down', 'position'], ('하측', 'NNG'):['down', 'position'],
             ('왼', 'NNG'):['left', 'position'], ('좌', 'NNG'):['left', 'position'], ('좌편', 'NNG'):['left', 'position'], ('좌측', 'NNG'):['left', 'position'],
             ('오른', 'NNG'):['right', 'position'], ('우측', 'NNG'):['right', 'position'], ('우편', 'NNG'):['right', 'position'],
             ('가운데', 'NNG'):['center', 'position'],
             #('첫', 'MM'):['1', 'num'], ('한', 'MM'):['1', 'num'], ('하나', 'NR'):['1', 'num'], ('일', 'NR'):['1', 'num'], ('1', 'SN'):['1', 'num'],
             #('두', 'MM'):['2', 'num'], ('이', 'NR'):['2', 'num'], ('둘', 'NR'):['2', 'num'], ('2', 'SN'):['2', 'num'],
             ('고', 'EC'):['and', 'sign'], ('그리고', 'MAJ'):['and', 'sign'], ('와', 'JKB'):['and', 'sign'], ('와', 'JC'):['and', 'sign'],
             ('없', 'VA'):['not', 'sign'],
             ('있', 'VV'):['exist', 'sign'], ('있', 'VA'):['exist', 'sign'], ('위치', 'NNG'):['exist', 'sign'], ('자리', 'NNG'):['exist', 'sign'], ('존재', 'NNG'):['exist', 'sign']}

kor_data = {"circle":"동그라미", "rect":"네모", "tri":"세모", "star":"별", "heart":"하트",
              "red":"빨간", "orange":"주황", "yellow":"노란", "green":"초록", "blue":"파란", "violet":"보라", "white":"흰", "black":"검은",
              "up":"위", "down":"아래", "left":"왼쪽", "right":"오른쪽", "center":"가운데"}

pos = Pororo(task="pos", lang="ko")

# 각 칸의 정보를 담을 dataclass
@dataclass
class Slot:
    figure: str = None
    color: str = None


def count_tag(tags, obj):
  val = 0
  for tag in tags:
    if obj in tag:
      val += 1
  return val


def create_grid():
  grid = []
  for i in range(9):
    grid.append(Slot())
  return grid


def add_case(cases, case):
  for i in range(len(case)):
    for slot in case[i+1:]:
      if case[i].color != None and case[i].figure != None and case[i] == slot:
        return False
  for onecase in cases:
    if case == onecase:
      return False
  cases.append(case)
  return True


def tagging(tags):
  inputs = []
  tag_stack = []
  sliced_tags = []
  start = 0
  for i in range(0, len(tags)):
    if tags[i][0] == 'and':
      sliced_tags.append(tags[start:i])
      start = i + 1
  if start < len(tags):
    sliced_tags.append(tags[start:len(tags)])

  for taglist in sliced_tags:
    if max(count_tag(taglist, "color"), count_tag(taglist, "figure")) == 2 and count_tag(taglist, "position") > 0:
      _color = None
      _figure = None
      _position = []
      _countF = 0
      _input = [[], [], [], True]
      for tag in taglist:
        if (tag == ['not', 'sign']):
          _countF += 1
        if (tag[1] == "color"):
          if (_figure != None or _color != None):
            _input[0] = [_color, _figure]
            _figure = None
          _color = tag[0]
        if (tag[1] == "figure"):
          if (_figure != None):
            _input[0] = [_color, _figure]
            _color = None
          _figure = tag[0]
        if (tag[1] == "position"):
          if (_figure != None or _color != None):
            _input[2] = [_color, _figure]
            _figure = None
            _color = None
          _position.append(tag[0])
      if (_figure != None or _color != None):
        _input[0] = [_color, _figure]
      _input[1] = _position
      _input[3] = (_countF % 2 == 0)
      inputs.append(_input)

      shape1 = ["","",""]
      shape2 = ["",""]

      if _input[0][0] != None:
        shape1[0] = kor_data[_input[0][0]]+" "
      if _input[0][1] == None:
        shape1[1] = "도형"
      else:
        shape1[1] = kor_data[_input[0][1]]

      if _input[2][0] != None:
        shape2[0] = kor_data[_input[2][0]]+" "
      if _input[2][1] == None:
        shape2[1] = "도형"
      else:
        shape2[1] = kor_data[_input[2][1]]

      for _p in _input[1]:
        shape1[2] += kor_data[_p]

      logtext.configure(state='normal')
      if _input[3]:
        logtext.insert("end", "[해석된 문장]: "+shape2[0]+shape2[1]+"의 "+shape1[2]+"에 "+shape1[0]+shape1[1]+"(이)가 있다.\n")
      else:
        logtext.insert("end", "[해석된 문장]: "+shape2[0]+shape2[1]+"의 "+shape1[2]+"에 "+shape1[0]+shape1[1]+"(은)는 없다.\n")
      logtext.see("end")
      logtext.configure(state='disabled')

    elif max(count_tag(taglist, "color"), count_tag(taglist, "figure")) == 1 and not (count_tag(taglist, "color") == 0 and count_tag(taglist, "figure") == 0):
      _color = None
      _figure = None
      _position = []
      _countF = 0
      for tag in taglist:
        if (tag == ['not', 'sign']):
          _countF += 1
        if (tag[1] == "color"):
          _color = tag[0]
        if (tag[1] == "figure"):
          _figure = tag[0]
        if (tag[1] == "position"):
          _position.append(tag[0])
      inputs.append([[_color, _figure], _position, [None, None], (_countF % 2 == 0)])

      shape1 = ["", "", ""]

      if _color != None:
        shape1[0] = kor_data[_color] + " "
      if _figure == None:
        shape1[1] = "도형"
      else:
        shape1[1] = kor_data[_figure]
      for _p in _position:
        shape1[2] += kor_data[_p]
      if len(_position)>0:
        shape1[2] += "에 "

      logtext.configure(state='normal')
      if _countF % 2 == 0:
        logtext.insert("end", "[해석된 문장]: "+shape1[0]+shape1[1]+"(이)가 "+shape1[2]+"있다.\n")
      else:
        logtext.insert("end", "[해석된 문장]: "+shape1[0]+shape1[1]+"(은)는 "+shape1[2]+"없다.\n")
      logtext.see("end")
      logtext.configure(state='disabled')

    else:
      logtext.configure(state='normal')
      logtext.insert("end", "[Error]: 해석할 수 없는 문장입니다.\n")
      logtext.see("end")
      logtext.configure(state='disabled')
      return False
  return inputs


def arrange(inputs):
  global possibility, negatives
  for log in inputs:
    if log[3]:
      newcase = []
      if log[1] == []:
        if len(possibility) == 0:
          for i in range(9):
            grid = create_grid()
            grid[i].color = log[0][0]
            grid[i].figure = log[0][1]
            add_case(newcase, grid)
        else:
          for case in possibility:
            for i in range(9):
              if (case[i].color == None or log[0][0] == None or case[i].color == log[0][0]) and (
                      case[i].figure == None or log[0][1] == None or case[i].figure == log[0][1]):
                grid = copy.deepcopy(case)
                if log[0][0] != None:
                  grid[i].color = log[0][0]
                if log[0][1] != None:
                  grid[i].figure = log[0][1]
                add_case(newcase, grid)
      elif log[2] == [None, None]:
        _position = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        if "up" in log[1]:
          _position = [i for i in _position if i in [0, 1, 2]]
        if "down" in log[1]:
          _position = [i for i in _position if i in [6, 7, 8]]
        if "left" in log[1]:
          _position = [i for i in _position if i in [0, 3, 6]]
        if "right" in log[1]:
          _position = [i for i in _position if i in [2, 5, 8]]
        if "center" in log[1]:
          if len(log[1]) == 1:
            _position = [4]
          else:
            _position = [i for i in _position if i not in [0, 2, 6, 8]]

        if len(possibility) == 0:
          for i in _position:
            grid = create_grid()
            grid[i].color = log[0][0]
            grid[i].figure = log[0][1]
            add_case(newcase, grid)
        else:
          for case in possibility:
            for i in _position:
              if (case[i].color == None or log[0][0] == None or case[i].color == log[0][0]) and (
                      case[i].figure == None or log[0][1] == None or case[i].figure == log[0][1]):
                grid = copy.deepcopy(case)
                if log[0][0] != None:
                  grid[i].color = log[0][0]
                if log[0][1] != None:
                  grid[i].figure = log[0][1]
                add_case(newcase, grid)
      else:
        _position = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        if "up" in log[1]:
          _position = [i for i in _position if i not in [0, 1, 2]]
        if "down" in log[1]:
          _position = [i for i in _position if i not in [6, 7, 8]]
        if "left" in log[1]:
          _position = [i for i in _position if i not in [0, 3, 6]]
        if "right" in log[1]:
          _position = [i for i in _position if i not in [2, 5, 8]]

        if len(possibility) == 0:
          for i in _position:
            grid = create_grid()
            grid[i].color = log[2][0]
            grid[i].figure = log[2][1]
            _subposition = []
            if "up" in log[1]:
              k = i - 3
              while k >= 0:
                _subposition.append(k)
                k -= 3
            if "down" in log[1]:
              k = i + 3
              while k < 9:
                _subposition.append(k)
                k += 3
            if "left" in log[1]:
              k = i - 1
              while k % 3 != 2:
                _subposition.append(k)
                k -= 1
            if "right" in log[1]:
              k = i + 1
              while k % 3 != 0:
                _subposition.append(k)
                k += 1
            for j in _subposition:
              grid2 = copy.deepcopy(grid)
              grid2[j].color = log[0][0]
              grid2[j].figure = log[0][1]
              add_case(newcase, grid2)
        else:
          for case in possibility:
            for i in _position:
              if (case[i].color == None or log[2][0] == None or case[i].color == log[2][0]) and (
                      case[i].figure == None or log[2][1] == None or case[i].figure == log[2][1]):
                grid = copy.deepcopy(case)
                if log[2][0] != None:
                  grid[i].color = log[2][0]
                if log[2][1] != None:
                  grid[i].figure = log[2][1]

                _subposition = []
                if "up" in log[1]:
                  k = i - 3
                  while k >= 0:
                    _subposition.append(k)
                    k -= 3
                if "down" in log[1]:
                  k = i + 3
                  while k < 9:
                    _subposition.append(k)
                    k += 3
                if "left" in log[1]:
                  k = i - 1
                  while k % 3 != 2:
                    _subposition.append(k)
                    k -= 1
                if "right" in log[1]:
                  k = i + 1
                  while k % 3 != 0:
                    _subposition.append(k)
                    k += 1
                for j in _subposition:
                  if (grid[j].color == None or log[0][0] == None or grid[j].color == log[0][0]) and (
                          grid[j].figure == None or log[0][1] == None or grid[j].figure == log[0][1]):
                    grid2 = copy.deepcopy(grid)
                    if log[0][0] != None:
                      grid2[j].color = log[0][0]
                    if log[0][1] != None:
                      grid2[j].figure = log[0][1]
                    add_case(newcase, grid2)

      possibility = newcase
    else:
      negatives.append(log)

  for neg in negatives:
    newcase = []
    for case in possibility:
      _check = True

      if neg[1] == []:
        for slot in case:
          if (neg[0][0] == None or neg[0][0] == slot.color) and (neg[0][1] == None or neg[0][1] == slot.figure):
            _check = False
            break

      elif neg[2] == [None, None]:
        _position = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        if "up" in neg[1]:
          _position = [i for i in _position if i in [0, 1, 2]]
        if "down" in neg[1]:
          _position = [i for i in _position if i in [6, 7, 8]]
        if "left" in neg[1]:
          _position = [i for i in _position if i in [0, 3, 6]]
        if "right" in neg[1]:
          _position = [i for i in _position if i in [2, 5, 8]]
        if "center" in neg[1]:
          if len(neg[1]) == 1:
            _position = [4]
          else:
            _position = [i for i in _position if i not in [0, 2, 6, 8]]

        for i in _position:
          if (neg[0][0] == None or neg[0][0] == case[i].color) and (neg[0][1] == None or neg[0][1] == case[i].figure):
            _check = False
            break

      else:
        for i in range(9):
          if (neg[2][0] == None or neg[2][0] == case[i].color) and (neg[2][1] == None or neg[2][1] == case[i].figure):
            _subposition = []
            if "up" in neg[1]:
              k = i - 3
              while k >= 0:
                _subposition.append(k)
                k -= 3
            if "down" in neg[1]:
              k = i + 3
              while k < 9:
                _subposition.append(k)
                k += 3
            if "left" in neg[1]:
              k = i - 1
              while k % 3 != 2:
                _subposition.append(k)
                k -= 1
            if "right" in neg[1]:
              k = i + 1
              while k % 3 != 0:
                _subposition.append(k)
                k += 1
            for j in _subposition:
              if (neg[0][0] == None or neg[0][0] == case[j].color) and (
                      neg[0][1] == None or neg[0][1] == case[j].figure):
                _check = False
                break
            if not _check:
              break


      if _check:
        newcase.append(case)
    possibility = newcase
    print(len(possibility))

  return possibility, negatives


def new_input(s):
  global possibility, negatives

  logtext.configure(state='normal')
  logtext.insert("end", "[입력된 문장]: "+s+"\n")
  logtext.see("end")
  logtext.configure(state='disabled')

  morphemes = pos(s)
  print(morphemes)
  tags = []

  # 유의미한 형태소만 태그로 정리
  for morpheme in morphemes:
    dic = word_data.get(morpheme)
    if dic:
      tags.append(dic)

  #print(tags)

  inputs = tagging(tags)

  if inputs:
    print(inputs)
    arrange(inputs)

    '''for case in possibility:
      for i in range(3):
        print(case[i * 3 + 0].color, case[i * 3 + 0].figure, "\t", case[i * 3 + 1].color, case[i * 3 + 1].figure, "\t",
              case[i * 3 + 2].color, case[i * 3 + 2].figure)
      print()

    print(len(possibility))'''


def buttonClicked(event):
  global possibility, stuck, resetCheck
  s = textinput.get()
  if s and not stuck:
    textinput.delete(0, "end")
    new_input(s)

    if len(possibility) > 0 and not resetCheck:
      resetCheck = True

    if len(possibility) >= 2:
      pos_queue = [[],[],[],[],[],[],[],[],[]]
      for case in possibility:
        for i in range(9):
          if (case[i].color != None or case[i].figure != None):
            f = case[i].figure
            if f == None:
              f = "none"
            c = case[i].color
            if c == None:
              c = "none"
            if (c, f) not in pos_queue[i]:
              pos_queue[i].append((c, f))

      print(pos_queue)

      for i in range(9):
        if len(pos_queue[i])==1:
          _count = 0
          for j in range(9):
            if pos_queue[i][0] in pos_queue[j]:
              _count += 1
          if _count == 1:
            for _s in small_label[i]:
              _s.place_forget()
            label[i+9].configure(image=big_images[pos_queue[i][0][1]][pos_queue[i][0][0]])
          else:
            for _s in small_label[i]:
              _s.place_forget()
            small_label[i][0].place(x=48 + 96 * ((i % 3) + 4), y=48 + 96 * (i// 3))
            small_label[i][0].configure(image=small_images[pos_queue[i][0][1]][pos_queue[i][0][0]])
        else:
          for j in range(9):
            if j < len(pos_queue[i]):
              c = pos_queue[i][j][0]
              if c == None:
                c = "none"
              f = pos_queue[i][j][1]
              if f == None:
                f = "none"
              small_label[i][j].place(x=48 + 96 * ((i % 3) + 4) + 32 * (j % 3), y=48 + 96 * (i// 3) + 32 * (j // 3))
              small_label[i][j].configure(image=small_images[f][c])
            else:
              small_label[i][j].place_forget()

    elif len(possibility) == 1:
      _check = True
      for i in range(9):
        for _s in small_label[i]:
          _s.place_forget()
        c = possibility[0][i].color
        if c == None:
          c = "none"
        f = possibility[0][i].figure
        if f == None:
          f = "none"
        label[i+9].configure(image=big_images[f][c])

        if not (possibility[0][i].color == target[i][0] and possibility[0][i].figure == target[i][1]):
          _check = False

      if _check:
        logtext.configure(state='normal')
        logtext.insert("end", "배치가 완벽하게 일치합니다.")
        logtext.see("end")
        logtext.configure(state='disabled')
        messagebox.showinfo(title="성공", message="배치가 완벽하게 일치합니다.")
        stuck = True

    elif resetCheck:
      logtext.configure(state='normal')
      logtext.insert("end", "[Error]: 불가능한 조건입니다. 더이상 진행할 수 없습니다. 초기화 후 다시 시도하세요.\n")
      logtext.see("end")
      logtext.configure(state='disabled')
      messagebox.showwarning(title="실패", message="불가능한 조건입니다. 더이상 진행할 수 없습니다. 초기화 후 다시 시도하세요.")
      stuck = True


def initValue():
  global possibility, negatives, resetCheck, stuck
  possibility = []
  negatives = []

  resetCheck = False
  stuck = False


def randomTarget():
  num = random.randrange(3, 8)
  target = [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None),
            (None, None), (None, None)]
  for i in range(num):
    while (True):
      f = figure_data[random.randrange(1, len(figure_data))]
      c = color_data[random.randrange(1, len(color_data))]
      if (c, f) not in target:
        j = random.randrange(0, 9)
        if target[j] == (None, None):
          target[j] = (c, f)
          break

  return target

def reset():
  initValue()

  target = randomTarget()
  for i in range(9):
    c = target[i][0]
    if c == None:
      c = "none"
    f = target[i][1]
    if f == None:
      f = "none"
    label[i].config(image=big_images[f][c])
    label[i].place(x=48 + 96 * (i % 3), y=48 + 96 * (i // 3))

  retry()


def retry():
  initValue()
  logtext.configure(state='normal')
  logtext.delete(1.0, "end")
  logtext.configure(state='disabled')
  for i in range(9):
    label[i+9].configure(image=big_images["none"]["none"])
    for j in range(9):
      small_label[i][j].place_forget()


# main
initValue()

window = Tk()

window.title("Shape Placement")
window.geometry("768x640+100+100")
window.resizable(False, False)

imageObj1 = []
imageObj2 = []
label = []
small_label = []

figure_data = ["none", "rect", "circle", "tri"]
color_data = ["none", "red", "orange", "yellow", "green", "blue", "violet", "white", "black"]
big_images = {}
small_images = {}

for f in figure_data:
  _big = {}
  _small = {}
  for c in color_data:
    _big[c] = PhotoImage(file="images/" + f + "_" + c + ".png")
    if not (f == "none" and c == "none"):
      _small[c] = PhotoImage(file="images/s_" + f + "_" + c + ".png")
  big_images[f] = _big
  small_images[f] = _small

target = randomTarget()

for i in range(18):
  if i < 9:
    c = target[i][0]
    if c == None:
      c = "none"
    f = target[i][1]
    if f == None:
      f = "none"
    label.append(Label(window, image=big_images[f][c]))
    label[i].place(x=48 + 96 * (i % 3), y=48 + 96 * (i // 3))
  else:
    label.append(Label(window, image=big_images["none"]["none"]))
    label[i].place(x=48 + 96 * ((i % 3) + 4), y=48 + 96 * ((i - 9) // 3))

    _small = []
    for j in range(9):
      _small.append(Label(window))
      _small[j].place(x=48 + 96 * ((i % 3) + 4) + 32 * (j % 3), y=48 + 96 * ((i - 9) // 3) + 32 * (j // 3))
      _small[j].place_forget()
    small_label.append(_small)

  textinput = Entry(window, width=64)
  textinput.place(x=80, y=360)

  btn = Button(window, height=1, width=10, text="입력")
  btn.bind("<Button-1>",buttonClicked)
  btn.place(x=600, y=356)
  window.bind('<Return>',buttonClicked)

  logtext = scrolledtext.ScrolledText(window, width=80, height=10)
  logtext.place(x=80, y=400)
  logtext.configure(state='disabled')

  menubar = Menu(window)
  menu_1 = Menu(menubar, tearoff = 0)
  menu_1.add_command(label="리셋", command=reset)
  menu_1.add_command(label="재시도", command=retry)
  menubar.add_cascade(label="초기화", menu=menu_1)

  window.config(menu = menubar)

window.mainloop()




