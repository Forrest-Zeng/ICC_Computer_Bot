from Equation import Expression
import urllib.parse, random, math


def quadratic(self, name):
  while True:
    a = random.randint(-10, 20)
    b = a * 2 * random.randint(-40, 40)
    c = None

    for i in range(-20, 40):
      if i == 0:
        continue
      discriminator = b**2 - 4 * a * i
      if discriminator > 0 and math.sqrt(
          discriminator) >= 0 and math.sqrt(discriminator) % (2 * a) == 0:
        c = i
        sqrt = math.sqrt(discriminator)
        answers = [int((-b + sqrt) / (2 * a)), int((-b - sqrt) / (2 * a))]
        if sqrt == 0:
          answers = [answers[0]]
        break

    if c != None:
      break
  
  answer = max(answers)

  distance = random.randint(0, abs(answer // 10) + 3)
  rank = random.randint(0, 3)
  return "https://latex.codecogs.com/png.latex?%5Cbg_white%20%5Cfn_cm%20%5Chuge%20%5Ctext%7B" + urllib.parse.quote(
      name.replace("\\", "")).replace("{", "%7B").replace("}", "%7D").replace(
          "^", "%5E") + "'s%20question%3A%7D" + urllib.parse.quote(
              (str([a, ""][a == 1]) + "x^2 " + "+-"[b < 0] + " " +
               str([b, -b][b < 0]) + "x " + "+-"[c < 0] + " " +
               str([c, -c][c < 0]) + " = 0").replace("-1", "-")), [answer + distance * (i - rank) for i in range(4)], rank

def math_equation(self, name):
  expressions = [
      "$*$", "$*$", "$+$", "$-$", "$-$", "$/@", "$^2", "$^3",
      "#sqrt(" + str(random.randint(30, 100)**2) + ")",
      "#sqrt(" + str(random.randint(100, 200)**2) + ")",
      "#sqrt(" + str(random.randint(200, 300)**2) + ")"
  ]

  equation = ""
  exponent = False

  for i in range(random.randint(1, 4)):
    if i == 0:
      while True:
        equation = random.choice(expressions)
        if not (exponent and "^" in equation):
          if "^" in equation:
            exponent = True
          elif exponent:
            exponent = False
          break
        if "^" in equation:
          exponent = True
      equation = equation.replace("#", "")
      for i in range(len(equation)):
        if equation[i] == "$":
          equation = equation[:i] + str(random.randint(1,
                                                       9)) + equation[i + 1:]
        elif equation[i] == "@":
          equation = equation[:i] + str(
              random.choice(["1", "2", "4", "5", "8"])) + equation[i + 1:]
    else:
      while True:
        expression = random.choice(expressions)
        if not (exponent and "^" in expression):
          if "^" in expression:
            exponent = True
          elif exponent:
            exponent = False
          break
      first = True

      for j in range(len(expression)):
        if expression[j] == "$" and first:
          first = False
        elif expression[j] == "$":
          equation += str(random.randint(1, 100))
        elif expression[j] == "@":
          equation += str(random.choice(["1", "2", "4", "5", "8", "10"]))
        elif expression[j] == "#":
          equation += random.choice("+-")
        else:
          equation += expression[j]

    equation = "(" + equation + ")"

  fn = Expression(equation)
  answer = fn()

  question = "https://latex.codecogs.com/png.latex?%5Cbg_white%20%5Cfn_cm%20%5Chuge%20%5Ctext%7B" + urllib.parse.quote(
      name.replace("\\", "")).replace("{", "%7B").replace("}", "%7D").replace(
          "^", "%5E") + "'s%20question%3A%7D" + urllib.parse.quote(
              str(fn))
  
  distance = random.randint(0, abs(answer // 10) + 3)
  rank = random.randint(0, 3)
  return question, [answer + distance * (i - rank) for i in range(4)], rank
