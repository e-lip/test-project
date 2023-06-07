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
        pen = QPen(QColor(255, 255, 255), 10)
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
        # self.curve_list.append(self.scene.items()[0])  # copy 해서 undo_list에 넣음으로 해결!


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