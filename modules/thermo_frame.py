#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################

from PyQt4.QtCore import QTimer, SIGNAL, SLOT, Qt, QPointF, QPoint, QRectF, QRect
from PyQt4.QtGui import  QMessageBox, QTextEdit, QDialog, QPolygonF,QPainter, QPen, QColor 
from PyQt4.QtGui import  QBrush, QMainWindow,QWidget,QToolTip,QApplication, QFont,QIcon,QAction
from PyQt4.QtGui import  QFrame,QListWidget,QComboBox,QCheckBox,QPushButton,QProgressBar,QLineEdit,QLabel
from PyQt4.QtGui import  QTextBrowser, QCursor, qApp, QDesktopWidget
from PyQt4.QtGui import  QGraphicsView, QGraphicsScene, QPicture, QPaintDevice, QStaticText

###################################################################################################
class ThermoFrame(QFrame):

    # =======================================================================
    def __init__(self, parent=None):

        # -------------------------------------------------------------------
        QFrame.__init__(self, parent);

        # -------------------------------------------------------------------
        self.setFrameShape( 0x0001 );
        """
        QFrame.NoFrame      0       QFrame draws nothing
        QFrame.Box          0x0001  QFrame draws a box around its contents
        QFrame.Panel        0x0002  QFrame draws a panel to make the contents appear raised or sunken
        QFrame.StyledPanel  0x0006  draws a rectangular panel with a look that depends on the current GUI style. It can be raised or sunken.
        QFrame.HLine        0x0004  QFrame draws a horizontal line that frames nothing (useful as separator)
        QFrame.VLine        0x0005  QFrame draws a vertical line that frames nothing (useful as separator)
        QFrame.WinPanel     0x0003  rectangular panel that can be raised or sunken like those in Windows 2000
        """

        # -------------------------------------------------------------------


        #self.setFrameStyle(QFrame.NoFrame);

        # -------------------------------------------------------------------
        self.PARENT                                 = parent;
        self.INITED                                 = False;
        self.ANTIALIASING                           = True;
        self.W                                      = 0;
        self.H                                      = 0;

        self.MATRIX                                 = {};
        self.MATRIX_W                               = 36;
        self.MATRIX_H                               = 61;
        self.PX_SIZE                                = [20, 10];
        self.BORDER_W                               = 2;
        self.ML                                     = 20;
        self.MT                                     = 30;
        
        self.setGeometry(self.ML, self.MT, self.MATRIX_W*self.PX_SIZE[0]+ (self.BORDER_W*2), self.MATRIX_H*self.PX_SIZE[1] + (self.BORDER_W*2) );
        self.setStyleSheet( "QFrame{ background-color: #000; color: #fff; border-style: solid; border-width: "+str(self.BORDER_W)+"px; border-color: #fff; }" );
        
        # -------------------------------------------------------------------
        self.BTNS_ML = self.MATRIX_W*self.PX_SIZE[0]+self.BORDER_W*2+30+self.ML;
        self.LABELS_STYLE = "QLabel{ color: #fff;}"

        # -----------------------------------
        # STATUS LABEL
        self.STATUS_LABEL_DISCONN = "QLabel{ color: #000; font-weight: bold; background-color: #F00; padding-left: 10px; line-height: 26px; }";
        self.STATUS_LABEL_CONN    = "QLabel{ color: #000; font-weight: bold; background-color: #FF0; padding-left: 10px; line-height: 26px; }";
        self.STATUS_LABEL_RUNNING = "QLabel{ color: #000; font-weight: bold; background-color: #0F0; padding-left: 10px; line-height: 26px; }";

        self.STATUS_LABEL                           = QLabel( "Disconnected" , self.PARENT);
        self.STATUS_LABEL.setStyleSheet( self.STATUS_LABEL_DISCONN );
        self.STATUS_LABEL.setGeometry( 280, 2, 200, 26 );

        # serial port
        self.SERIAL_PORT_INPUT_LABEL                = QLabel( "Serial port:" , self.PARENT);
        self.SERIAL_PORT_INPUT_LABEL.setGeometry( self.BTNS_ML+5, self.MT+0, 200, 25 );
        self.SERIAL_PORT_INPUT_LABEL.setStyleSheet( self.LABELS_STYLE );

        self.SERIAL_PORT_INPUT                      = QLineEdit( self.PARENT.SERIAL_PORT , self.PARENT);
        self.SERIAL_PORT_INPUT.setGeometry( self.BTNS_ML, self.MT+25, 200, 25 );

        # -----------------------------------
        # serial baudrate
        self.SERIAL_BAUDRATE_INPUT_LABEL                = QLabel( "Baudrate: (speed e.g 9600)" , self.PARENT);
        self.SERIAL_BAUDRATE_INPUT_LABEL.setGeometry( self.BTNS_ML+5, self.MT+50, 200, 25 );
        self.SERIAL_BAUDRATE_INPUT_LABEL.setStyleSheet( self.LABELS_STYLE );

        self.SERIAL_BAUDRATE_INPUT                  = QLineEdit( str(self.PARENT.SERIAL_BAUDRATE) , self.PARENT);
        self.SERIAL_BAUDRATE_INPUT.setGeometry( self.BTNS_ML, self.MT+75, 200, 25 );

        # -----------------------------------
        # serial timeout
        self.SERIAL_TIMEOUT_INPUT_LABEL                = QLabel( "Serial timeout:" , self.PARENT);
        self.SERIAL_TIMEOUT_INPUT_LABEL.setGeometry( self.BTNS_ML+5, self.MT+100, 200, 25 );
        self.SERIAL_TIMEOUT_INPUT_LABEL.setStyleSheet( self.LABELS_STYLE );

        self.SERIAL_TIMEOUT_INPUT                  = QLineEdit( str(self.PARENT.SERIAL_TIMEOUT) , self.PARENT);
        self.SERIAL_TIMEOUT_INPUT.setGeometry( self.BTNS_ML, self.MT+125, 200, 25 );

        # -----------------------------------
        # buttons
        self.CONNECT_BTN                            = QPushButton("Connect", self.PARENT);
        self.CONNECT_BTN.setGeometry( self.BTNS_ML, self.MT+165, 200, 25 );
        self.CONNECT_BTN.clicked.connect( self.CONNECT );


        self.START_BTN                              = QPushButton("Start", self.PARENT);
        self.START_BTN.setGeometry( self.BTNS_ML, self.MT+195, 200, 25 );
        self.START_BTN.clicked.connect( self.START );

        self.STOP_BTN                               = QPushButton("Stop", self.PARENT);
        self.STOP_BTN.setGeometry( self.BTNS_ML, self.MT+225, 200, 25 );
        self.STOP_BTN.clicked.connect( self.STOP );

        self.HEAD_UP_BTN                            = QPushButton("HEAD-UP: (10)", self.PARENT);
        self.HEAD_UP_BTN.setGeometry( self.BTNS_ML, self.MT+300, 200, 25 );
        self.HEAD_UP_BTN.clicked.connect( self.PARENT.HEAD_UP );

        self.HEAD_DN_BTN                            = QPushButton("HEAD-DOWN: (10)", self.PARENT);
        self.HEAD_DN_BTN.setGeometry( self.BTNS_ML, self.MT+330, 200, 25 );
        self.HEAD_DN_BTN.clicked.connect( self.PARENT.HEAD_DOWN );


        # -------------------------------------------------------------------
        self.arrow_style = "QLabel{ font-size: 14px; font-weight: bold; color: #F00; }";
        self.SCAN_POS_ARROW_L_ML = self.ML-10;
        self.SCAN_POS_ARROW_L_MT = self.MT+2;

        self.SCAN_POS_ARROW_L                       = QLabel(u"█", self.PARENT);
        self.SCAN_POS_ARROW_L.setStyleSheet( self.arrow_style );
        self.SCAN_POS_ARROW_L.setGeometry( self.SCAN_POS_ARROW_L_ML, self.SCAN_POS_ARROW_L_MT, 10, 10 );

        self.SCAN_POS_ARROW_R_ML = self.ML+self.MATRIX_W*self.PX_SIZE[0]+self.BORDER_W*3;
        self.SCAN_POS_ARROW_R_MT = self.MT+2;

        self.SCAN_POS_ARROW_R                       = QLabel(u"█", self.PARENT);
        self.SCAN_POS_ARROW_R.setStyleSheet( self.arrow_style );
        self.SCAN_POS_ARROW_R.setGeometry( self.SCAN_POS_ARROW_R_ML, self.SCAN_POS_ARROW_R_MT, 10, 10 );

        # -------------------------------------------------------------------
        self._CANDEL_G_COLOR                        = QColor(0,225,0, 255 );
        self._CANDEL_R_COLOR                        = QColor(225,0,0, 255 );

        # -------------------------------------------------------------------
        self.INIT();

        # -------------------------------------------------------------------
    
    # =======================================================================
    def CONNECT(self):

        # -------------------------------------------------------------------
        self.PARENT.SERIAL_PORT     = str(self.SERIAL_PORT_INPUT.text() );
        self.PARENT.SERIAL_BAUDRATE = int( self.SERIAL_BAUDRATE_INPUT.text() );
        self.PARENT.SERIAL_TIMEOUT  = float( self.SERIAL_TIMEOUT_INPUT.text() );

        if self.PARENT.CONNECT():
            self.STATUS_LABEL.setText("Connected");
            self.STATUS_LABEL.setStyleSheet( self.STATUS_LABEL_CONN );

        else:
            self.STATUS_LABEL.setText("Disconnected");
            self.STATUS_LABEL.setStyleSheet( self.STATUS_LABEL_DISCONN );

        # -------------------------------------------------------------------

    # =======================================================================
    def START(self):

        # -------------------------------------------------------------------
        if self.PARENT.START():
            self.STATUS_LABEL.setText("Running");
            self.STATUS_LABEL.setStyleSheet( self.STATUS_LABEL_RUNNING );

        else:
            self.STATUS_LABEL.setText("Disconnected");
            self.STATUS_LABEL.setStyleSheet( self.STATUS_LABEL_DISCONN );

        # -------------------------------------------------------------------

    # =======================================================================
    def STOP(self):

        # -------------------------------------------------------------------
        if self.PARENT.STOP():
            self.STATUS_LABEL.setText("Connected");
            self.STATUS_LABEL.setStyleSheet( self.STATUS_LABEL_CONN );

        # -------------------------------------------------------------------

    # =======================================================================
    def INIT( self ):

        # -------------------------------------------------------------------
        try:

            row = 0;

            while row < self.MATRIX_H:
                self.MATRIX[ "_"+str(row) ] = [53 for x in xrange(self.MATRIX_W)]
                row += 1;


            self.show();
            self.INITED = True;

        except Exception as _err:

            self.EXCEPT( "", _err );

        # -------------------------------------------------------------------

    # =======================================================================
    def poly(self, _pts):
        
        pass;
        """
        for x in xrange(0, len(_pts)):
            if self._CANDELS[x][0] == None:
                self._CANDELS[x][0] = 0;
            if self._CANDELS[x][1] == None:
                self._CANDELS[x][1] = 0;

        return QPolygonF(map(lambda p: QPointF(*p), _pts))
        """

    # =======================================================================
    def paintEvent(self, event):

        # -------------------------------------------------------------------
        Painter = QPainter()
        Painter.begin(self)
        #Painter.restore();
        # -------------------------------------------------------------------
        if self.ANTIALIASING:
            
            Painter.setRenderHint(Painter.Antialiasing);

        # -------------------------------------------------------------------
        Painter.setPen(QPen(QColor("#333333"), 0)); # main canvas bg

        for row in self.MATRIX:

            row_num = int(row.replace("_", ""));

            for row_index in xrange(0, len( self.MATRIX[row] )):
                
                """
                Painter.setBrush(QBrush( QColor( self.MATRIX[row][row_index], 0, self.MATRIX[row][row_index] ) )); # QColor( 255, 100, 20 )
                """

                if self.MATRIX[row][row_index] < 50: # blue
                    Painter.setBrush(QBrush( QColor( 0, 0, self.MATRIX[row][row_index] ) )); # QColor( 255, 100, 20 )

                elif self.MATRIX[row][row_index] < 100: # purple
                    Painter.setBrush(QBrush( QColor( self.MATRIX[row][row_index], 0, self.MATRIX[row][row_index] ) )); # QColor( 255, 100, 20 )

                elif self.MATRIX[row][row_index] < 150: # orange
                    Painter.setBrush(QBrush( QColor( self.MATRIX[row][row_index], int(self.MATRIX[row][row_index]/2), 0) )); # QColor( 255, 100, 20 )

                elif self.MATRIX[row][row_index] < 200: # yellow 
                    Painter.setBrush(QBrush( QColor( self.MATRIX[row][row_index], self.MATRIX[row][row_index], 0 ) )); # QColor( 255, 100, 20 )

                else: # white                    
                    Painter.setBrush(QBrush( QColor( self.MATRIX[row][row_index], self.MATRIX[row][row_index], int(self.MATRIX[row][row_index]/2 ) ) )); # QColor( 255, 100, 20 )

                    
                Painter.drawRect( self.BORDER_W+row_index*self.PX_SIZE[0], self.BORDER_W+row_num*self.PX_SIZE[1], self.PX_SIZE[0], self.PX_SIZE[1]);

        # -------------------------------------------------------------------
        #Painter.save();
        Painter.end();
        # -------------------------------------------------------------------

    # =======================================================================
    def UPDATE_ROW( self ):

        # -------------------------------------------------------------------
        try:

            tmp = self.PARENT.MATRIX_ROW.split("|");
            row = "_"+tmp[0];

            self.SCAN_POS_ARROW_L.setGeometry( self.SCAN_POS_ARROW_L_ML, self.SCAN_POS_ARROW_L_MT + (self.PX_SIZE[1]*int(tmp[0])), 10, 10 );
            self.SCAN_POS_ARROW_R.setGeometry( self.SCAN_POS_ARROW_R_ML, self.SCAN_POS_ARROW_R_MT + (self.PX_SIZE[1]*int(tmp[0])), 10, 10 );

            raw_data = tmp[1].split(",");

            data = [];

            for i in xrange(0, self.MATRIX_W):

                ii = raw_data[i].strip();
                if ii != "":
                    self.MATRIX[ "_"+tmp[0]][i] =  int( ii );

            self.update();

        except Exception as _err:
            self.EXCEPT( "UPDATE_ROW: ", _err );

        # -------------------------------------------------------------------

    # =======================================================================
    def UPDATE( self ):

        # -------------------------------------------------------------------
        # 60|76,66,67,64,69,71,73,75,75,73,72,74,|105,104,104,103,103,102,103,103,103,103,103,103,|89,84,81,83,81,80,80,79,79,80,79,79,
        # -------------------------------------------------------------------
        with open("data.list", "r") as FS:

            for LL in FS:

                tmp = LL.split("|");
                row = "_"+tmp[0];

                raw_data = tmp[1].split(",");

                data = [];

                for i in raw_data:

                    i = i.strip();
                    if i != "":
                        data.append( int(i.strip()));

                self.MATRIX[ "_"+tmp[0]] = data;

        # -------------------------------------------------------------------
        self.update();
        # -------------------------------------------------------------------

    # =======================================================================
    def EXCEPT(self, _info="no-info", _exception=""):

        # -------------------------------------------------------------------
        print( str(_info)+" : "+str(_exception) );
        # -------------------------------------------------------------------

    # =======================================================================

###################################################################################################
