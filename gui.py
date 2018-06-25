import sys  # sys нужен для передачи argv в QApplication
import design  # Это наш конвертированный файл дизайна

from PyQt5 import QtCore, QtGui, QtWidgets
import fireSearch as fire
from PIL import Image
import files as file


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    pachImage = None
    pachFireImage = None
    pachPossibleFireImage = None
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py

        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        # при нажатии кнопки
        self.pushButton.clicked.connect(self.SetPachImage)
        self.pushButton_2.clicked.connect(self.SetFireImage)
        self.pushButton_3.clicked.connect(self.SetPossibleFireImage)
        self.pushButton_4.clicked.connect(self.starting)
        self.pushButton_5.clicked.connect(self.clearLog)
        self.pushButton_6.clicked.connect(self.SaveLog)



    def starting(self):

        if self.pachImage == None or self.pachFireImage == None or self.pachPossibleFireImage == None:
            print("Не все параметры заданны")
            self.listWidget.addItem("Не все параметры заданны")
        else:
            listImage = file.getDataFolder(self.pachImage)
            value = 0
            self.progressBar.setValue(value)
            self.progressBar.setMaximum(len(listImage))

            for i in range(0, len(listImage)):

                print("Осталось обработать: " + str(len(listImage) - i))
                print("Имя изображения: " + listImage[i])
                self.listWidget.addItem("Имя изображения: " + listImage[i])

                im = Image.open(self.pachImage + '/' + listImage[i])
                searchFire = fire.getFireSearch(im, self.spinBox.value())

                value = value + 1
                self.progressBar.setValue(value)
                # [0] - РАзмер изображения
                # [1] - Координаты пожара
                # [2] - Максимальная температура
                # [3] - Преобразованная матрица
                #return ((c, b), (fireJ, fireI), MaxT, T)
                self.listWidget.addItem('Размер изображения: ' + str(searchFire[0][0])+"x"+str(searchFire[0][1]))
                self.listWidget.addItem('Максимальная интенсивность: ' + str(searchFire[2]))

                if (searchFire[2] > 180):
                    print('Обработка по температуре: Пожар')
                    self.listWidget.addItem('Обработка по температуре: Пожар')
                    if (fire.fireMaxT(searchFire[3], searchFire[0][0], searchFire[0][1], self.spinBox_3.value(),self.spinBox_3.value(), self.spinBox_2.value()) == 1):
                        print("Обработка по площади: Пожар")
                        self.listWidget.addItem("Обработка по площади: Пожар")
                        im.save(self.pachFireImage +"/" + listImage[i])
                    else:
                        print("Обработка по площади: Нет пожара")
                        self.listWidget.addItem("Обработка по площади: Нет пожара")
                elif (searchFire[2] > 80):
                    print('Обработка по температуре: Возможен пожар')
                    self.listWidget.addItem('Обработка по температуре: Возможен пожар')
                    if (fire.fireMaxT(searchFire[3], searchFire[0][0], searchFire[0][1], self.spinBox_3.value(),self.spinBox_3.value(), self.spinBox_2.value()) == 1):
                        print("Обработка по площади: Пожар")
                        self.listWidget.addItem("Обработка по площади: Пожар")
                        im.save(self.pachFireImage + "/" + listImage[i])
                    else:
                        print("Обработка по площади: Нет пожара")
                        self.listWidget.addItem("Обработка по площади: Нет пожара")
                        im.save(self.pachPossibleFireImage + "/" + listImage[i])
                else:
                    print('Обработка по температуре: нет пожара')
                    self.listWidget.addItem('Обработка по температуре: нет пожара')

                j = 0
                for q in searchFire[1][0]:
                    maxIntensiv = im.getpixel((j,q))[0]
                    print("интенсивность")
                    print(maxIntensiv)
                    self.listWidget.addItem("Точка: " + str(int(q)) + ", " + str(int(searchFire[1][1][j])) +" интенсивность: " + str(maxIntensiv))
                    j = j + 1

                self.listWidget.addItem('__________________________________________')

                im.close()

    def clearLog(self):
        self.listWidget.clear()

    def SaveLog(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить LOG')
        print(name)
        file = open(name[0], 'w')
        for i in range(0, len(self.listWidget)):
            text = self.listWidget.item(i).text()
            print(text)
            file.write(str(text) + "\n")
        file.close()

    def SetPachImage(self):

        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории

        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            self.pachImage = directory
            self.label_4.setText(str(len(file.getDataFolder(self.pachImage)))+" штук")

    def SetFireImage(self):

        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории
        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            self.pachFireImage = directory

    def SetPossibleFireImage(self):

        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории
        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            self.pachPossibleFireImage = directory



def main():
    QtGui.QGuiApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()