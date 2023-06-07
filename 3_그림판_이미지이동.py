import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_ui()


    def set_ui(self):
        # 0. vbox : 전체 위젯이 들어감
        self.vbox = QVBoxLayout()

        # 1. hbox1 : 버튼 기능(이미지 불러오기, 실행취소, 다시실행)과 파일명이 들어감
        self.hbox1 = QHBoxLayout()

        # 1.1. 버튼1 : 이미지 불러오기
        self.btn_img = QPushButton(self)
        icon = self.style().standardIcon(QStyle.SP_FileIcon)
        self.btn_img.setIcon(icon)
        self.btn_img.setFixedSize(40, 40)
        self.btn_img.clicked.connect(self.load_img)

        # 1.2. 버튼2 : 실행취소
        self.undo_img = QPushButton(self)
        icon = self.style().standardIcon(QStyle.SP_ArrowBack)
        self.undo_img.setIcon(icon)
        self.undo_img.setFixedSize(40, 40)

        # 1.3. 버튼3 : 다시실행
        self.redo_img = QPushButton(self)
        icon = self.style().standardIcon(QStyle.SP_ArrowForward)
        self.redo_img.setIcon(icon)
        self.redo_img.setFixedSize(40, 40)

        # 1.4. 버튼4 : 이미지 저장
        self.save_img = QPushButton(self)
        icon = self.style().standardIcon(QStyle.SP_DialogSaveButton)
        self.save_img.setIcon(icon)
        self.save_img.setFixedSize(40, 40)
        self.save_img.clicked.connect(self.save_image)


        # 1.5. 파일명
        self.img_title = QLabel('파일명')
        self.img_title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        self.img_title.setFont(font)
        self.img_title.setMinimumHeight(70)

        # 1.6. 위젯 추가
        self.hbox1.addWidget(self.btn_img)
        self.hbox1.addWidget(self.save_img)
        self.hbox1.addWidget(self.undo_img)
        self.hbox1.addWidget(self.redo_img)
        self.hbox1.addWidget(self.img_title)


        # 2. hbox2 : 그림판의 메뉴 툴바(왼쪽)와 그림판 영역(오른쪽)이 들어감
        self.hbox2 = QHBoxLayout()

        # 2.1. vbox2 : 메뉴툴바(왼쪽)
        self.vbox2 = QVBoxLayout()

        # 2.1.1. group_box1 : 펜종류
        group_box1 = QGroupBox('그리기 종류')
        self.vbox2.addWidget(group_box1)

        # 그룹박스 1 에서 사용할 레이아웃
        pen_box = QVBoxLayout()
        group_box1.setLayout(pen_box)

        # 그룹박스 1 의 라디오 버튼 배치
        text = ['line', 'Curve', 'Rectange', 'Ellipse']
        self.radio_btns = []
        for i in range(len(text)):
            self.radio_btns.append(QRadioButton(text[i], self))
            self.radio_btns[i].clicked.connect(self.radio_clicked)
            pen_box.addWidget(self.radio_btns[i])
        self.radio_btns[0].setChecked(True)
        self.draw_type = 0

        # 2.1.2. group_box2 : 펜 굵기와 색상
        group_box2 = QGroupBox('펜 설정')
        self.vbox2.addWidget(group_box2)

        grid = QGridLayout()
        group_box2.setLayout(grid)

        label = QLabel('선굵기')
        grid.addWidget(label, 0, 0)
 
        self.combo = QComboBox()
        grid.addWidget(self.combo, 0, 1)       
 
        for i in range(1, 21):
            self.combo.addItem(str(i))
 
        label = QLabel('선색상')
        grid.addWidget(label, 1,0)        
         
        self.pencolor = QColor(0,0,0)
        self.pen_btn = QPushButton()        
        self.pen_btn.setStyleSheet('background-color: rgb(0,0,0)')
        self.pen_btn.clicked.connect(self.show_color_dialog)
        grid.addWidget(self.pen_btn,1, 1)


        # 2.1.3. group_box3 : 채우기 색상
        group_box3 = QGroupBox('채우기 설정')        
        self.vbox2.addWidget(group_box3)

        box1 = QHBoxLayout()
        group_box3.setLayout(box1)
 
        label = QLabel('채우기 색상')
        box1.addWidget(label)                
 
        self.brushcolor = QColor(255,255,255)
        self.brush_btn = QPushButton()        
        self.brush_btn.setStyleSheet('background-color: rgb(255,255,255)')
        self.brush_btn.clicked.connect(self.show_color_dialog)
        box1.addWidget(self.brush_btn)


        # 2.1.4. group_box4 : 지우개
        group_box4 = QGroupBox('지우개')        
        self.vbox2.addWidget(group_box4)
 
        box2 = QHBoxLayout()
        group_box4.setLayout(box2)        
         
        self.checkbox = QCheckBox('지우개 동작')
        box2.addWidget(self.checkbox)
 
        self.vbox2.addStretch()      


        # 2.2 이미지 로드 및 그림판 영역
        self.view = Canvas(self)       
        self.hbox2.addLayout(self.vbox2)
        self.hbox2.addWidget(self.view)


        # 3. 전체 위젯 설정
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.vbox)
        self.setCentralWidget(self.central_widget)


        # 프로그램의 위치 및 크기 설정
        self.setGeometry(300, 200, 1500, 1100)
        self.setWindowTitle('MyApp')
        self.show()



    def radio_clicked(self):
        for i in range(len(self.radio_btns)):
            if self.radio_btns[i].isChecked():
                self.draw_type = i                
                break



    def show_color_dialog(self):        
        # 색상 대화상자 생성      
        color = QColorDialog.getColor()
        sender = self.sender()
 
        # 색상이 유효한 값이면 참, QFrame에 색 적용
        if sender == self.pen_btn and color.isValid():           
            self.pencolor = color
            self.pen_btn.setStyleSheet('background-color: {}'.format( color.name()))
        else:
            self.brushcolor = color
            self.brush_btn.setStyleSheet('background-color: {}'.format( color.name()))



    def load_img(self):
        open_file = QFileDialog.getOpenFileName(self, '이미지 열기', './', filter='Images (*.png *.jpg)')

        self.pixmap = QPixmap(open_file[0])
        # self.view.scene.addPixmap(self.pixmap)
        pixmap_item = self.view.scene.addPixmap(self.pixmap)
        image_rect = pixmap_item.boundingRect()
        self.view.setSceneRect(image_rect)



    def save_image(self):
        # 뷰포트 영역의 사이즈를 가져옴
        full_rect = self.view.scene.itemsBoundingRect()

        # 임시 이미지 생성
        image = QImage(full_rect.size().toSize(), QImage.Format_ARGB32)
        image.fill(Qt.transparent)

        # QPainter를 사용하여 뷰포트 영역을 이미지로 그림
        painter = QPainter(image)
        self.view.scene.render(painter, QRectF(image.rect()), QRectF(full_rect))


        # 이미지를 파일로 저장
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg);;All Files (*)", options=options)
        if file_path:
            image.save(file_path)




# canvas : 그림이 그려지는 영역 
class Canvas(QGraphicsView):
    def __init__(self, window):
        super().__init__(window)
    
        self.scene = QGraphicsScene()        
        self.setScene(self.scene)

        self.items = []     
        self.m_start = QPointF()
        self.m_end = QPointF()
 
        self.setRenderHint(QPainter.HighQualityAntialiasing)

        #
        self.image_item = None
        self.last_mouse_pos = None



    def moveEvent(self, e):
        rect = QRectF(self.rect())
        rect.adjust(0,0,-2,-2)
 
        self.scene.setSceneRect(rect)



    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            # 시작점 저장
            self.m_start = self.mapToScene(e.pos())
            self.m_end = self.mapToScene(e.pos())

            #
            if e.modifiers() == Qt.ControlModifier:
                # Ctrl 키와 함께 마우스 왼쪽 버튼을 눌렀을 때 이미지 이동 모드로 설정
                self.last_mouse_pos = e.pos()
            else:
                self.last_mouse_pos = None
        super().mousePressEvent(e)



    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.m_end = self.mapToScene(e.pos())

            #
            if self.last_mouse_pos is not None:
                delta = e.pos() - self.last_mouse_pos
                self.last_mouse_pos = e.pos()
                # 이미지 이동
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())

            if e.modifiers() != Qt.ControlModifier:
                # Ctrl 키를 누르지 않은 경우에만 그림 그리기

                if self.window().checkbox.isChecked():
                    pen = QPen(QColor(255, 255, 255), 10)
                    path = QPainterPath()
                    path.moveTo(self.m_start)
                    path.lineTo(self.m_end)
                    self.scene.addPath(path, pen)
                    self.m_start = self.mapToScene(e.pos())
                    return None

                pen = QPen(self.window().pencolor, self.window().combo.currentIndex())

                if self.window().draw_type == 0:
                    if len(self.items) > 0:
                        self.scene.removeItem(self.items[-1])
                        del self.items[-1]
                    line = QLineF(self.m_start, self.m_end)
                    self.items.append(self.scene.addLine(line, pen))

                if self.window().draw_type == 1:
                    path = QPainterPath()
                    path.moveTo(self.m_start)
                    path.lineTo(self.m_end)
                    self.scene.addPath(path, pen)
                    self.m_start = self.mapToScene(e.pos())

                if self.window().draw_type == 2:
                    brush = QBrush(self.window().brushcolor)
                    if len(self.items) > 0:
                        self.scene.removeItem(self.items[-1])
                        del self.items[-1]
                    rect = QRectF(self.m_start, self.m_end)
                    self.items.append(self.scene.addRect(rect, pen, brush))

                if self.window().draw_type == 3:
                    brush = QBrush(self.window().brushcolor)
                    if len(self.items) > 0:
                        self.scene.removeItem(self.items[-1])
                        del self.items[-1]
                    rect = QRectF(self.m_start, self.m_end)
                    self.items.append(self.scene.addEllipse(rect, pen, brush))
        
        super().mouseMoveEvent(e)

 

    def mouseReleaseEvent(self, e):        
        if e.button() == Qt.LeftButton: 
            if self.window().checkbox.isChecked():
                return None
 
            pen = QPen(self.window().pencolor, self.window().combo.currentIndex())
 
            if self.window().draw_type == 0:
                self.items.clear()
                line = QLineF(self.m_start.x(), self.m_start.y(), self.m_end.x(), self.m_end.y())
                 
                self.scene.addLine(line, pen)
 
            if self.window().draw_type == 2:
                brush = QBrush(self.window().brushcolor)
 
                self.items.clear()
                rect = QRectF(self.m_start, self.m_end)
                self.scene.addRect(rect, pen, brush)
 
            if self.window().draw_type == 3:
                brush = QBrush(self.window().brushcolor)
 
                self.items.clear()
                rect = QRectF(self.m_start, self.m_end)
                self.scene.addEllipse(rect, pen, brush)
            
            #
            self.last_mouse_pos = None
        super().mouseReleaseEvent(e)



    def wheelEvent(self, event):
        # Ctrl 키가 눌려있을 때만 확대 및 축소 수행
        if event.modifiers() == Qt.ControlModifier:
            # 휠 이벤트의 각각의 값이 120의 배수로 전달되므로, 120으로 나눠서 스케일 팩터를 조정
            delta = event.angleDelta().y() / 120

            # 휠 위로 굴리면 확대, 아래로 굴리면 축소
            new_scale = 1.1 if delta > 0 else 1 / 1.1  

            # 최소 스케일과 최대 스케일 값을 설정 (선택적으로 사용)
            min_scale = 0.1
            max_scale = 5.0
            new_scale = max(min_scale, min(new_scale, max_scale))

            # 이미지를 중앙을 기준으로 스케일 조정
            self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
            self.scale(new_scale, new_scale)

        else:
            # Ctrl 키가 눌려있지 않을 때에는 기본 동작 수행
            super().wheelEvent(event)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())