PI = 3.1415926563


def number_input():
    output = input('input number : ')
    return float(output)

def get_circumferrence(radius):
    return 2 * PI * radius
def get_circle_area(radius):
    return PI * radius **2

#단위 테스트 출력용으로 적합 

if __name__ is '__main__' :
    print(get_circumferrence(8))
    print(get_circle_area(8))