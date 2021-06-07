import numpy as np
import cv2

# 색상 테이블
hsvData_l = [] # HSV 영역을 제한하기 위한 최솟값(Lower)
hsvData_u = [] # HSV 영역을 제한하기 위한 최대값(Upper)
hsvData_l.append((0, 80, 80)) # 빨강
hsvData_u.append((5, 255, 255))
hsvData_l.append((30, 80, 80)) # 초록
hsvData_u.append((70, 255, 255))
hsvData_l.append((100, 80, 80)) # 파랑
hsvData_u.append((140, 255, 255))
hsvData_l.append((0, 0, 255)) # 흰색
hsvData_u.append((0, 64, 255))

circleCountMax = 100 # 공의 최대 검출 개수

def searchCircle(img_back, hsv_l, hsv_u): # 공을 찾는 함수
    img = cv2.imread('Image/Ball1.jpg', cv2.IMREAD_COLOR) # 이미지 읽기
    img_resize = cv2.resize(img, (540, 960), interpolation = cv2.INTER_CUBIC) # 리사이즈
    img_hsv = cv2.cvtColor(img_resize, cv2.COLOR_BGR2HSV) # HSV 영역으로 변환
    img_range = cv2.inRange(img_hsv, hsv_l, hsv_u) # 특정 영역의 색상 추출
    img_gb = cv2.GaussianBlur(img_range, (13, 13), 0) # 노이즈 제거 및 엣지 검출에 용이하기 위해 가우시안 필터 적용

    param2_num = 21 # param2 초기값

    while True: # param2 값을 조정하기 위한 While문
        circles = cv2.HoughCircles(img_gb, cv2.HOUGH_GRADIENT, 1, 30, param1=60, param2=param2_num, minRadius=0, maxRadius=100) # 허프 원 변환을 이용하여 원 검출
        print(param2_num)
        circleCount = 0

        if circles is not None:
            circles = np.uint16(np.around(circles)) # 원들 좌표를 반올림

            for i in circles[0, :]: # 검출된 원의 개수만큼 반복
                circleCount += 1 # 원 개수 카운팅

            if circleCount < circleCountMax: # 만약 검출된 원이 최대 원 개수 미만이면
                for i in circles[0, :]:
                    cv2.circle(img_back, (i[0], i[1]), i[2], (255, 255, 0), 2)
                print("원의 개수 : ", circleCount)
                return img_resize, img_back, circleCount
        else:
            print("원을 찾을 수 없음")

        if param2_num > 50:
            print("원을 찾을 수 없어 프로그램을 종료합니다. ")
            break
        else:
            param2_num += 1

    return img_resize, img_back, circleCount


def main():
    circleTotal = 0
    img_back = np.zeros((960, 540, 3), np.uint8) # 원 표시용 빈 이미지 생성

    for i in range(0, len(hsvData_l)): # 위에서 지정한 색상테이블별로 추출
        img, img_back, count = searchCircle(img_back, hsvData_l[i], hsvData_u[i])
        circleTotal += count # 총 개수

    print("원의 총 개수 : ", circleTotal)

    text = "Found Ball : " + str(circleTotal)
    cv2.putText(img, text, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))
    cv2.imshow('H-Circle', cv2.add(img, img_back)) # 출력
    k = cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

