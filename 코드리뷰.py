import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# 애플리케이션의 UI 요소가 고해상도 디스플레이에서 더 잘 보이도록 조정
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        self.create_widgets()
        self.setup_layout()

        # 프로그램의 위치 및 크기 설정
        self.setGeometry(300, 200, 1500, 1100)
        self.setWindowTitle('MyApp')
        self.show()


    def create_button(self, icon_type, tooltip):
        button = QPushButton(self)
        icon = self.style().standardIcon(icon_type)
        button.setIcon(icon)
        button.setFixedSize(40, 40)
        button.setToolTip(f'{tooltip}')
        return button
    

    def create_widgets(self):
        # btn_img_load : 이미지 불러오기
        self.btn_img_load = self.create_button(QStyle.SP_DialogOpenButton, '이미지 불러오기')
        self.btn_img_load.clicked.connect(self.load_img)
        shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        shortcut.activated.connect(self.load_img)

        # btn_img_save : 이미지 저장하기
        self.btn_img_save = self.create_button(QStyle.SP_FileIcon, '이미지 저장')
        self.btn_img_save.clicked.connect(self.save_image)
        shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        shortcut.activated.connect(self.save_image)

        # btn_undo_action : 실행취소
        self.btn_undo_action = self.create_button(QStyle.SP_ArrowBack, '실행 취소')
        self.btn_undo_action.clicked.connect(self.undo_action)
        shortcut = QShortcut(QKeySequence('Ctrl+Z'), self)
        shortcut.activated.connect(self.undo_action)

        # btn_redo_action : 다시실행
        self.btn_redo_action = self.create_button(QStyle.SP_ArrowForward, '다시 실행')
        self.btn_redo_action.clicked.connect(self.redo_action)
        shortcut = QShortcut(QKeySequence('Ctrl+Y'), self)
        shortcut.activated.connect(self.redo_action)

        # img_title : 파일명
        self.img_title = QLabel('파일명')
        self.img_title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        self.img_title.setFont(font)
        self.img_title.setMinimumHeight(70)


        # pen_type_group_box : 펜 종류
        self.pen_type_group_box = QGroupBox('그리기 종류')
        pen_box = QVBoxLayout()
        self.pen_type_group_box.setLayout(pen_box)

        text = ['Line', 'Cureve', 'Rectange', 'Ellipse']
        self.radio_btns = []
        for i in range(len(text)):
            self.radio_btns.append(QRadioButton(text[i], self))
            self.radio_btns[i].clicked.connect(self.radio_clicked)
            pen_box.addWidget(self.radio_btns[i])
        self.radio_btns[0].setChecked(True)
        self.draw_type = 0


        # pen_setting_group_box : 펜의 선 굵기와 색상 설정
        self.pen_setting_group_box = QGroupBox('펜 설정')

        grid = QGridLayout()
        self.pen_setting_group_box.setLayout(grid)

        label = QLabel('선굵기')
        grid.addWidget(label, 0, 0)

        self.combo = QComboBox()
        grid.addWidget(self.combo, 0, 1)

        for i in range(1, 20 + 1):
            self.combo.addItem(str(i))

        label = QLabel('선색상')
        grid.addWidget(label, 1, 0)

        self.pen_color = QColor(0, 0, 0)
        self.pen_btn = QPushButton()
        self.pen_btn.setStyleSheet('background-color: rgb(0,0,0)')
        self.pen_btn.clicked.connect(self.show_color_dialog)
        grid.addWidget(self.pen_btn, 1, 1)

 
        # fill_color_group_box : 채우기 색상
        self.fill_color_group_box = QGroupBox('채우기 설정')        

        temp_box1 = QHBoxLayout()
        self.fill_color_group_box.setLayout(temp_box1)
 
        label = QLabel('채우기 색상')
        temp_box1.addWidget(label)                
 
        self.brush_color = QColor(255,255,255)
        self.brush_btn = QPushButton()        
        self.brush_btn.setStyleSheet('background-color: rgb(255,255,255)')
        self.brush_btn.clicked.connect(self.show_color_dialog)
        temp_box1.addWidget(self.brush_btn)


        # eraser_group_box : 지우개
        self.eraser_group_box = QGroupBox('지우개')        
 
        temp_box2 = QHBoxLayout()
        self.eraser_group_box.setLayout(temp_box2)        
         
        self.checkbox = QCheckBox('지우개 동작')
        temp_box2.addWidget(self.checkbox)


    def load_img(self):
        open_file = QFileDialog.getOpenFileName(self, '이미지 열기', './', filter='Images (*.png *.jpg)')
        self.pixmap = QPixmap(open_file[0])
        pixmap_item = self.paint_area.scene.addPixmap(self.pixmap)
        image_rect = pixmap_item.boundingRect()
        self.paint_area.setSceneRect(image_rect)


    def save_image(self):
        # 뷰포트 영역의 사이즈를 가져옴
        full_rect = self.paint_area.scene.itemsBoundingRect()

        # 임시 이미지 생성
        image = QImage(full_rect.size().toSize(), QImage.Format_ARGB32)
        image.fill(Qt.transparent)  # 이미지를 투명하게 채움

        # QPainter를 사용하여 뷰포트 영역을 이미지로 그림
        painter = QPainter(image)
        self.paint_area.scene.render(painter, QRectF(image.rect()), QRectF(full_rect))

        # 그리기 작업 완료 및 리소스 정리
        painter.end()

        # 이미지를 파일로 저장
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'Images (*.png *.jpg);;All Files (*)', options=options)

        if file_path:
            image.save(file_path)

        # 저장 완료 메시지 표시
        QMessageBox.information(self, '저장 완료', '이미지가 성공적으로 저장되었습니다.', QMessageBox.Ok)

        # 프로그램 종료
        self.close()


    def undo_action(self):
        if self.paint_area.undo_list:
            item = self.paint_area.undo_list.pop()
            self.paint_area.redo_list.append(item)

            if isinstance(item, list):
                for i in item:
                    self.paint_area.scene.removeItem(i)
            else:
                self.paint_area.scene.removeItem(item)
        # print(f'items : {self.paint_area.scene.items()}')
        # print(f'undo_list : {self.paint_area.undo_list}')


    
    def redo_action(self):
        if self.paint_area.redo_list:
            item = self.paint_area.redo_list.pop()  
            self.paint_area.undo_list.append(item)

            if isinstance(item, list):
                for i in item:
                    self.paint_area.scene.addItem(i)  
            else:
                self.paint_area.scene.addItem(item)


    def radio_clicked(self):
        for i in range(len(self.radio_btns)):
            if self.radio_btns[i].isChecked():
                self.draw_type = i                
                break


    def show_color_dialog(self):
        # 색상 대화상자 생성
        color = QColorDialog.getColor()
        sender = self.sender()  # 메소드를 호출한 객체(즉, 클릭된 버튼)를 저장

        # 색상이 유효한 값이면 참, QFrame에 색 적용
        if sender == self.pen_btn and color.isValid():
            self.pen_color = color
            self.pen_btn.setStyleSheet(f'background-color : {color.name()}')
        elif sender == self.brush_btn and color.isValid():
            self.brush_color = color
            self.brush_btn.setStyleSheet(f'background-color : {color.name()}')
        else:
            pass



    def setup_layout(self):
        # button_hbox : 최상단 버튼기능 + 파일명이 표시되는 영역
        button_hbox = QHBoxLayout()
        button_hbox.addWidget(self.btn_img_load)
        button_hbox.addWidget(self.btn_img_save)
        button_hbox.addWidget(self.btn_undo_action)
        button_hbox.addWidget(self.btn_redo_action)
        button_hbox.addWidget(self.img_title)

        # paint_menu_vbox : 그림판의 메뉴가 있는 영역 (펜종류, 색 등)
        paint_menu_vbox = QVBoxLayout()
        paint_menu_vbox.addWidget(self.pen_type_group_box)
        paint_menu_vbox.addWidget(self.pen_setting_group_box)
        paint_menu_vbox.addWidget(self.fill_color_group_box)
        paint_menu_vbox.addWidget(self.eraser_group_box)
        paint_menu_vbox.addStretch()  

        # 그림판 영역
        self.paint_area = Canvas(self)

        # paint_hbox : 그림판 메뉴와 그림판을 묶은 영역
        paint_hbox = QHBoxLayout()
        paint_hbox.addLayout(paint_menu_vbox)
        paint_hbox.addWidget(self.paint_area)
        
        # main_vbox : 전체 프로그램의 레이아웃이 형성되는 영역
        main_vbox = QVBoxLayout()
        main_vbox.addLayout(button_hbox)
        main_vbox.addLayout(paint_hbox)

        central_widget = QWidget(self)
        central_widget.setLayout(main_vbox)
        self.setCentralWidget(central_widget)



class Canvas(QGraphicsView):
    def __init__(self, window):
        super().__init__(window)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.items = []
        self.undo_list = []
        self.redo_list = []
        self.curve_list = []

        self.m_start = QPointF()
        self.m_end = QPointF()

        self.setRenderHint(QPainter.HighQualityAntialiasing)
        self.image_itme = None
        self.last_mouse_pos = None

    
    def moveEvent(self, e):
        rect = QRectF(self.rect())
        rect.adjust(0, 0, -2, -2)
        self.scene.setSceneRect(rect)


    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            # 시작점 저장 (마우스 이벤트의 좌표를 QGraphicsView의 좌표계에서 QGraphicsScene의 좌표계로 변환)
            self.m_start = self.mapToScene(e.pos())
            self.m_end = self.mapToScene(e.pos())

            if e.modifiers() == Qt.ControlModifier:
                # Ctrl 키와 함께 마우스 왼쪽 버튼을 눌렀을 떄 이미지 이동 모드로 설정
                self.last_mouse_pos = e.pos()
            else:
                self.last_mouse_pos = None
        super().mousePressEvent(e)


    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.m_end = self.mapToScene(e.pos())

            if self.last_mouse_pos is not None:
                delta = e.pos() - self.last_mouse_pos
                self.last_mouse_pos = e.pos()
                # 이미지 이동
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())

            if e.modifiers() != Qt.ControlModifier:
                if self.window().checkbox.isChecked():
                    self.draw_eraser(e)
                else:
                    self.draw_shape(e)
        super().mouseMoveEvent(e)


    def draw_eraser(self, e):
        pen = QPen(QColor(255, 255, 255), 20)
        path = QPainterPath()
        path.moveTo(self.m_start)
        path.lineTo(self.m_end)
        self.scene.addPath(path, pen)
        self.m_start = self.mapToScene(e.pos())



    def draw_shape(self, e):
        pen = QPen(self.window().pen_color, self.window().combo.currentIndex())
        if self.window().draw_type == 0:
            self.draw_line(pen)
        elif self.window().draw_type == 1:
            self.draw_curve(pen, e)
        elif self.window().draw_type == 2:
            self.draw_rectangle(pen)
        elif self.window().draw_type == 3:
            self.draw_ellipse(pen)

    
    def draw_line(self, pen):
        if len(self.items) > 0:
            self.scene.removeItem(self.items[-1])
            del self.items[-1]
        line = QLineF(self.m_start, self.m_end)
        self.items.append(self.scene.addLine(line, pen))

    
    def draw_curve(self, pen, e):
        path = QPainterPath()
        path.moveTo(self.m_start)
        path.lineTo(self.m_end)
        self.scene.addPath(path, pen)
        self.m_start = self.mapToScene(e.pos())
        self.curve_list.append(self.scene.items()[0])  # copy 해서 undo_list에 넣음으로 해결!


    def draw_rectangle(self, pen):
        brush = QBrush(self.window().brush_color)
        if len(self.items) > 0:
            self.scene.removeItem(self.items[-1])
            del self.items[-1]
        rect = QRectF(self.m_start, self.m_end)
        self.items.append(self.scene.addRect(rect, pen, brush))


    def draw_ellipse(self, pen):
        brush = QBrush(self.window().brush_color)
        if len(self.items) > 0:
            self.scene.removeItem(self.items[-1])
            del self.items[-1]
        rect = QRectF(self.m_start, self.m_end)
        self.items.append(self.scene.addEllipse(rect, pen, brush))


    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.window().checkbox.isChecked():
                return None           
            pen = QPen(self.window().pen_color, self.window().combo.currentIndex()) 
            if self.window().draw_type == 0:
                self.items.clear()
                self.undo_list.append(self.scene.items()[0])
            elif self.window().draw_type == 1:
                self.undo_list.append(self.curve_list.copy())
                self.curve_list.clear()                     
            elif self.window().draw_type == 2:
                self.items.clear()
                self.undo_list.append(self.scene.items()[0])
            elif self.window().draw_type == 3:
                self.items.clear()
                self.undo_list.append(self.scene.items()[0])
            self.last_mouse_pos = None
        super().mouseReleaseEvent(e)


    def wheelEvent(self, event):
        # Ctrl 키가 눌려있을 때만 확대 및 축소 수행
        if event.modifiers() == Qt.ControlModifier:
            # 휠 이벤트의 각각의 값이 120의 배수로 전달되므로, 120으로 나눠서 스케일 팩터를 조정
            delta = event.angleDelta().y() / 120

            # 휠 위로 굴리면 확대, 아래로 굴리면 축소
            new_scale = 1.1 if delta > 0 else 1 / 1.1

            # 최소 스케일과 최대 스케일 값을 설정
            min_scale = 0.1
            max_scale = 5.0
            new_scale = max(min_scale, min(new_scale, max_scale))

            # 이미지 중앙을 기준으로 스케일 조정
            self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
            self.scale(new_scale, new_scale)

        else:
            # Ctrl 키가 눌려있지 않은 경우에는 기본 동작 수행!!
            super().wheelEvent(event)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())