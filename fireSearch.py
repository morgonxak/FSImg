import numpy
import matplotlib.pyplot as plt


def getFireSearch(image, TmT):
    fireJ = numpy.zeros(0)# масив для хранения точек с пожароси
    fireI = numpy.zeros(0)

    (c, b) = image.size

    T = numpy.zeros(image.size)
    #print(type(image.getpixel((0,0)))) #<class 'tuple'> - старые ихображения
                                       #<class 'int'> - новые ихображения

    if str(type(image.getpixel((0,0)))) == "<class 'tuple'>":
        boolTypeImage = True

    else:
        boolTypeImage = False


    #plt.imshow(image)
    #plt.show()

    Tma = TmT
    Tmi = -10

    tT = (Tma - Tmi) / 255

    for j in range(0, c - 1):
        for i in range(0, b - 1):
            if boolTypeImage:
                T[j, i] = Tmi + (image.getpixel((j, i))[0] + image.getpixel((j, i))[1] + image.getpixel((j, i))[2]) / 3 * tT
            else:
                T[j, i] = Tmi + (image.getpixel((j, i)) + image.getpixel((j, i)) + image.getpixel((j, i))) / 3 * tT

            if T[j,i] == TmT:
                fireJ = numpy.append(fireJ,j)
                fireI = numpy.append(fireI,i)


    MaxT = numpy.max(T)

    #[0] - РАзмер изображения
    #[1] - Координаты пожара
    #[2] - Максимальная температура
    #[3] - Преобразованная матрица
    return ((c,b),(fireJ,fireI),MaxT,T)

def test():
    from PIL import Image
    import files as file
    pachImage = 'image/' + file.getDataFolder()[0]
    im = Image.open(pachImage)
    res = getFireSearch(im, 200)
    print(res[1][0])
    print(res[2])


'''

    #########################################################
    X=10
    Y=10
    S = 0.1

    #########################################################
    if (MaxT > 180):
        print('Обработка по температуре: Пожар')
        if fireMaxT(T, c, b, X, Y, S) == 1:
            return 2
        else:
            return 0
    elif(MaxT > 80):
        print('Обработка по температуре: Возможен пожар')
        if fireMaxT(T, c, b, X, Y, S) == 1:
            return 2
        else:
            return 1
    else:
        print('Обработка по температуре: нет пожара')
        return 0
'''
def fireMaxT(T,c,b,X,Y,S):
    dSP = X * Y / c / b
    mPt = 0
    for i in range(0,c-1):
        for j in range(0,b-1):
            if T[i,j]>180:
                mPt = mPt + 1

    SP = dSP * mPt
    print("SP: "+str(SP))
    print("mPt: "+str(mPt))
    print("dSP: " + str(dSP))
    if SP > S:
        print("Обработка по площади: Пожар")
        return 1
    else:
        print("Обработка по площади: Нет Пожара")
        return 0



if __name__ == '__main__':  # Program start from here
    try:
        test()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        print("СП")