from PyQt5 import QtWidgets , QtCore, QtGui
from pyqtgraph import plot, PlotWidget
import pyqtgraph as pg
import sys  
import os
import os.path
import main_gui
from fourier_transform import fourier , spectro_range
import pandas as pd
from scipy import signal
import numpy as np
from PyQt5.QtWidgets import QMessageBox , QFileDialog
from PyQt5.Qt import QFileInfo
from scipy.io import wavfile
import sounddevice as sd
import time
from pdf import GeneratePDF
import pyqtgraph.exporters
from scipy.io.wavfile import write


class MainWindow(QtWidgets.QMainWindow , main_gui.Ui_MainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        #########variables######################
        #####timers for plots####

        self.timer=  [ 0 ] 

        self.interval = [0]
        ###index for dynamic plot
        self.index = [ 0 ]
        ####### list for slider
        self.gain = [10 * [1]]
        
        #1st comment: variables names
        self.slider_list = [self.gainSlider_1, self.gainSlider_2, self.gainSlider_3, self.gainSlider_4, self.gainSlider_5, self.gainSlider_6, self.gainSlider_7,
        self.gainSlider_8, self.gainSlider_9, self.gainSlider_10]
        for i in range(10):
            self.gain[0][i] = float(self.slider_list[i].value())/10
        ######plot configuration#####
        self.pen = pg.mkPen(color=(255, 0, 0))
        # for i in sel
        self.widget_configuration(self.widget_before1 , "Input signal 1")
        self.widget_configuration(self.widget_after1 , "Output signal 1")
        self.widget_configuration(self.widget_1s , "Spectrogram 1")

        self.input_graph = [

            self.widget_before1

        ]
        self.output_graph = [
            self.widget_after1
        ]
        self.spectro_widgets = [

            self.widget_1s,

        ]
        for i in self.spectro_widgets:
            i.hide()
        
        self.spectro_min = [0]
        self.spectro_max = [1]

        self.current_tab_index = 0  ###indicate current widget index

        #####color palette for spectro gram
        self.color =[ [(0.5, (0, 182, 188, 255)),
                        (1.0, (246, 111, 0, 255)),
                        (0.0, (75, 0, 113, 255))]

                        ,[(0.5, (170, 0, 0, 255)),
                        (1.0, (0, 0, 255, 255)),
                        (0.0, (170, 255, 255, 255))]

                        ,[(0.5, (0, 255, 0, 255)),
                        (1.0, (170, 170, 255, 255)),
                        (0.0, (255, 85, 0, 255))]

                        ,[(0.5, (0, 255, 0, 255)),
                        (1.0, (85, 0, 255, 255)),
                        (0.0, (0, 255, 127, 255))]

                        ,[(0.5, (0, 0, 255, 255)),
                        (1.0, (170, 255, 127, 255)),
                        (0.0, (255, 255, 127, 255))] ]

        self.current_color = [0]
        #####aflag to indicate which is shown signal graph(1) or spectrogram(0) 
        
        self.spectro_flag = [0]
        
        self.signals = [0] #list to store loaded signals
        self.file_name = [0]
        self.input_signal = [0]
        self.freq_sampling = [0]
        self.output_signal = [0]
        self.i = 2
        self.tab ={}
        self.layout = {}
        self.actionColor = [self.actionColor_1, self.actionColor_2, self.actionColor_3, self.actionColor_4 , self.actionColor_5]
        #start the programm with one signal viewed

        #########actions triggeration###########
        self.tabWidget.tabCloseRequested.connect(lambda index: self.close_tab(index))
        for i in range(10):
            self.set_slider_function(i)
        
        # self.gainSlider_1.valueChanged.connect(lambda: self.get_gain(0))
        # self.gainSlider_2.valueChanged.connect(lambda: self.get_gain(1))
        # self.gainSlider_3.valueChanged.connect(lambda: self.get_gain(2))
        # self.gainSlider_4.valueChanged.connect(lambda: self.get_gain(3))
        # self.gainSlider_5.valueChanged.connect(lambda: self.get_gain(4))
        # self.gainSlider_6.valueChanged.connect(lambda: self.get_gain(5))
        # self.gainSlider_7.valueChanged.connect(lambda: self.get_gain(6))
        # self.gainSlider_8.valueChanged.connect(lambda: self.get_gain(7))
        # self.gainSlider_9.valueChanged.connect(lambda: self.get_gain(8))
        # self.gainSlider_10.valueChanged.connect(lambda: self.get_gain(9))
        self.spectro_minimum_slider.valueChanged.connect(self.update_spectro)
        self.spectro_maximum_slider.valueChanged.connect(self.update_spectro)
        self.tabWidget.currentChanged.connect(self.select)
        self.actionOpen.triggered.connect(self.openfile)
        self.actionSave_as_PDF.triggered.connect(self.export_pdf)
        self.actionToolbar.triggered.connect(self.toggle_tool)
        self.actionStatus_bar.triggered.connect(self.toggle_status)
        self.actionPlay.triggered.connect(self.play)
        self.actionPause.triggered.connect(self.pause)
        self.actionStop.triggered.connect(self.stop)
        self.actionClose.triggered.connect(self.close)
        self.actionFaster.triggered.connect(lambda:self.playback(1))
        self.actionSlower.triggered.connect(lambda:self.playback(-1))
        self.actionZoom_in.triggered.connect(lambda: self.zoom(1/1.25))
        self.actionZoom_out.triggered.connect(lambda: self.zoom(1.25))
        self.actionSpectrogram.triggered.connect(self.spectro)
        self.actionNew_tab.triggered.connect(self.new_tab)
        for i in range(5):
            self.set_color_function(i)

        
        # self.actionColor_1.triggered.connect(lambda:self.color_palette(0))
        # self.actionColor_2.triggered.connect(lambda:self.color_palette(1))
        # self.actionColor_3.triggered.connect(lambda:self.color_palette(2))
        # self.actionColor_4.triggered.connect(lambda:self.color_palette(3))
        # self.actionColor_5.triggered.connect(lambda:self.color_palette(4))
        self.actionAbout.triggered.connect(self.pop_up)
        self.actionExit.triggered.connect(lambda: sys.exit())
        self.actionScroll_right.triggered.connect(lambda:self.scroll_x(1))
        self.actionScroll_left.triggered.connect(lambda:self.scroll_x(-1))
        self.actionScroll_up.triggered.connect(lambda:self.scroll_y(1))
        self.actionScroll_down.triggered.connect(lambda:self.scroll_y(-1))
        self.pushButton.clicked.connect(self.play_sound)
        # self.actionSave.triggered.connect(self.save_audio)
    #2nd comment: code repitition
    def set_slider_function(self , i):
        self.slider_list[i].valueChanged.connect(lambda: self.get_gain(i))
    #2nd comment: code repitition
    def set_color_function(self ,i):
        self.actionColor[i].triggered.connect(lambda:self.color_palette(i))
    def close_tab(self , index):
        self.tabWidget.removeTab(index)
        self.input_graph.pop(index)
        self.output_graph.pop(index)
        self.spectro_widgets.pop(index)
        self.current_color.pop(index)
        self.spectro_flag.pop(index) 
        self.signals.pop(index) 
        self.file_name.pop(index) 
        self.input_signal.pop(index) 
        self.freq_sampling.pop(index) 
        self.output_signal.pop(index) 
        self.spectro_min.pop(index)
        self.spectro_max.pop(index)
        self.timer.pop(index)
        self.interval.pop(index)
        self.index.pop(index)
        self.gain.pop(index)
        
    def select(self):
        self.current_tab_index = self.tabWidget.currentIndex( )
        print(self.current_tab_index)
        if self.signals[self.current_tab_index] == 0 :
            self.disable_items()
        else:
            self.enable_items()
        for i in range(10):
            self.slider_list[i].setValue(self.gain[self.current_tab_index][i]*10)

        self.spectro_minimum_slider.setValue(self.spectro_min[self.current_tab_index]* 100)
        self.spectro_maximum_slider.setValue(self.spectro_max[self.current_tab_index] * 100)
        


    def get_gain(self , i):
        if self.signals[self.current_tab_index] != 0:
            self.gain[self.current_tab_index][i] =  float(self.slider_list[i].value())/10
            if self.df.isin([self.file_name[self.current_tab_index]]).any().any() :
                index = self.df.index[self.df['name'] == self.file_name[self.current_tab_index]].tolist()[0]
                self.df.iloc[index,1:] = self.gain[self.current_tab_index]
                # print(self.df)
            else :
                self.df.loc[len(self.df)] = [self.file_name[self.current_tab_index]] + self.gain[self.current_tab_index]
            # print(self.gain[self.current_tab_index][i])
            self.df.to_csv('sliders.csv')

            self.plot_output()

            self.plot_spectro(self.output_signal[self.current_tab_index] , self.color[self.current_color[self.current_tab_index]])
            y_range = self.input_graph[self.current_tab_index].getViewBox().state['viewRange'][1]
            self.output_graph[self.current_tab_index].setYRange(y_range[0] * self.gain[self.current_tab_index][i] , y_range[1] * self.gain[self.current_tab_index][i],padding=0)
            
        
       



        
    #####to load and plot signal#######
    def openfile(self):
        self.file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',"", "Data files (*.csv *.wav)")
        print(self.current_tab_index)
        
        if self.file_path:
            if self.file_path.endswith('.wav') :  ### to read .wav file
                
                self.data = wavfile.read(self.file_path)
                # self.sample_rate = self.data.getframerate()
                # print (self.sample_rate)
                audio_df = pd.DataFrame(self.data)
                # print(audio_df.head())
                self.freq_sampling[self.current_tab_index] = audio_df.iloc[0 , 0]
                self.input_signal[self.current_tab_index] = audio_df.iloc[1 , 0]
                # print(self.freq_sampling , self.input_signal[self.current_tab_index])
            else:
                df = pd.read_csv(self.file_path)
                self.input_signal[self.current_tab_index] = df.iloc[:,0]
                self.freq_sampling[self.current_tab_index] = 1000

            self.signals[self.current_tab_index] = self.file_path
            self.file_name[self.current_tab_index] = os.path.basename(self.signals[self.current_tab_index])

            self.reset_widget()
    
            self.plot_input()
            self.plot_output()
            self.enable_items()
            self.moving()
            self.update_sliders()
            self.spectro_sliders()
            self.plot_spectro(self.output_signal[self.current_tab_index],self.color[0]) #to create spectrogram
            
    def update_sliders(self):
        if os.path.isfile('sliders.csv'):
            self.df = pd.read_csv('sliders.csv', index_col=0)
            # print(df)
            # print(self.file_name)
            # print(df.isin([self.file_name]).any().any())
            if self.df.isin([self.file_name[self.current_tab_index]]).any().any() :
                self.gain[self.current_tab_index] = self.df[self.df['name'] == self.file_name[self.current_tab_index]].values.tolist()[0][1:]
                # print(len(self.gain[self.current_tab_index]))
                # print(len(self.slider_list))
            for i in range(10):
                self.slider_list[i].setValue(self.gain[self.current_tab_index][i]*10)

        else:
            data = [self.file_name[self.current_tab_index]] +  self.gain[self.current_tab_index]
            self.df = pd.DataFrame(data ).transpose()
            self.df.columns = ['name','gain_1','gain_2','gain_3','gain_4','gain_5','gain_6','gain_7','gain_8','gain_9','gain_10']
            # print(self.df)
            self.df.to_csv('sliders.csv')



    def plot_input(self):
        self.limits(self.input_graph[self.current_tab_index], self.input_signal[self.current_tab_index])
        self.input_graph[self.current_tab_index].plot(self.input_signal[self.current_tab_index],name = self.file_name[self.current_tab_index] ,pen=self.pen)

    def plot_output(self):
        # print(self.gain[self.current_tab_index] )
        self.output_signal[self.current_tab_index], z = fourier(self.input_signal[self.current_tab_index] , self.gain[self.current_tab_index])
        self.output_graph[self.current_tab_index].clear()
        self.output_graph[self.current_tab_index].plot(self.output_signal[self.current_tab_index] ,name = self.file_name[self.current_tab_index] ,pen=self.pen)
        self.limits(self.output_graph[self.current_tab_index], self.output_signal[self.current_tab_index])
        

    def moving(self):
        ##### create a timer for widgets#####
        self.index[self.current_tab_index] = 0
        self.interval[self.current_tab_index] = 25
        self.timer[self.current_tab_index] = QtCore.QTimer()
        self.timer[self.current_tab_index].setInterval(50)
        i = self.current_tab_index
        self.timer[i].timeout.connect(lambda:self.update_plot(i))
        # if self.current_tab_index == 0:
        #     # self.timer[0] = QtCore.QTimer()
        #     # self.timer[0].setInterval(10)
        #     self.timer[0].timeout.connect(self.update_plot1)

        # elif self.current_tab_index == 1:
        #     # self.timer[1] = QtCore.QTimer()
        #     # self.timer[1].setInterval(50)
        #     self.timer[1].timeout.connect(self.update_plot2)

        # else:
        #     # self.timer[2] = QtCore.QTimer()
        #     # self.timer[2].setInterval(50)
        #     self.timer[2].timeout.connect(self.update_plot3)
        self.timer[self.current_tab_index].start()
    
   

    def enable_items(self):
            
        ######enable tools to control signal#####
        self.actionZoom_in.setEnabled(True)
        self.actionZoom_out.setEnabled(True)
        self.actionPlay.setEnabled(True)
        self.actionPause.setEnabled(True)
        self.actionStop.setEnabled(True)
        self.actionClose.setEnabled(True)
        self.actionFaster.setEnabled(True)
        self.actionSlower.setEnabled(True)
        self.actionSpectrogram.setEnabled(True)
        self.actionScroll_right.setEnabled(True)
        self.actionScroll_left.setEnabled(True)
        self.actionScroll_up.setEnabled(True)
        self.actionScroll_down.setEnabled(True)
        self.actionColor_1.setEnabled(True)
        self.actionColor_2.setEnabled(True)
        self.actionColor_3.setEnabled(True)
        self.actionColor_4.setEnabled(True)
        self.actionColor_5.setEnabled(True)
        self.actionSave_as_PDF.setEnabled(True)
        self.pushButton.setEnabled(True)
        for i in range(10):
            self.slider_list[i].setEnabled(True)
        self.spectro_minimum_slider.setEnabled(True)
        self.spectro_maximum_slider.setEnabled(True)

            

    ########update function to make the plot moving###### 
    def update_plot(self , i):

        if self.signals[i] != 0:
            self.index[i] = self.index[i] + self.interval[i]
            self.input_graph[i].setXRange(0 + self.index[i], 5000 + self.index[i], padding=0)
            self.output_graph[i].setXRange(0 + self.index[i], 5000 + self.index[i], padding=0)

    # def update_plot2(self):

    #     if self.signals[1] != 0:
    #         self.index[1] = self.index[1] + self.interval[self.current_tab_index]
    #         self.graphs_widgets[1].setXRange(0 + self.index[1], 5000 + self.index[1], padding=0)
    #         self.graphs_widgets[4].setXRange(0 + self.index[1], 5000 + self.index[1], padding=0)

    # def update_plot3(self):                    
    #     if self.signals[2] != 0:
    #         self.index[2] = self.index[2] + self.interval[self.current_tab_index]
    #         self.graphs_widgets[2].setXRange(0 + self.index[2], 5000 + self.index[2], padding=0)
    #         self.graphs_widgets[5].setXRange(0 + self.index[2], 5000 + self.index[2], padding=0)
                    
    #######play function to start the movement####
    def play(self):
        
        if self.timer[self.current_tab_index] != 0 :
            self.limits(self.output_graph[self.current_tab_index], self.output_signal[self.current_tab_index])
            self.timer[self.current_tab_index].start()

    #######pause function to pause the movement####
    def pause(self):
      
        if self.timer[self.current_tab_index] != 0 :
            self.timer[self.current_tab_index].stop()
            print(self.current_tab_index)

    #######stop function to stop the movement and reset the signal plot####
    def stop(self):
    
        if self.timer[self.current_tab_index] != 0 :
            self.timer[self.current_tab_index].stop()
            self.index[self.current_tab_index] = 0
            self.input_graph[self.current_tab_index].setXRange(0, 5000, padding=0)
            self.output_graph[self.current_tab_index].setXRange(0, 5000, padding=0)
    def playback(self , sign):
        if self.interval[self.current_tab_index] < 45 and self.interval[self.current_tab_index] > 5:
            self.interval[self.current_tab_index] += (sign * 10)
            print(self.interval[self.current_tab_index])
            self.timer[self.current_tab_index].setInterval(self.interval[self.current_tab_index])
    # def slower(self):
    #     if self.interval[self.current_tab_index] > 5 :
    #         self.interval[self.current_tab_index] -= 10
    #         print(self.interval[self.current_tab_index])
    #         self.timer[self.current_tab_index].setInterval(self.interval[self.current_tab_index])
    #######close function to clear the plot####
    def close(self):
 
        self.timer[self.current_tab_index] = 0
        self.signals[self.current_tab_index] = 0
        self.reset_widget()
        self.disable_items()

    def play_sound(self):
        # print(self.output_signal[self.current_tab_index])
        duration = len(self.output_signal[self.current_tab_index]) / self.freq_sampling[self.current_tab_index]                
        sd.play(self.output_signal[self.current_tab_index],self.freq_sampling[self.current_tab_index])
        time.sleep(duration)
        sd.stop

    def disable_items(self):
        self.actionZoom_in.setEnabled(False)
        self.actionZoom_out.setEnabled(False)
        self.actionPlay.setEnabled(False)
        self.actionPause.setEnabled(False)
        self.actionStop.setEnabled(False)
        self.actionClose.setEnabled(False)
        self.actionSpectrogram.setEnabled(False)
        self.actionScroll_right.setEnabled(False)
        self.actionScroll_left.setEnabled(False)
        self.actionScroll_up.setEnabled(False)
        self.actionScroll_down.setEnabled(False)
        self.actionColor_1.setEnabled(False)
        self.actionColor_2.setEnabled(False)
        self.actionColor_3.setEnabled(False)
        self.actionColor_4.setEnabled(False)
        self.actionColor_5.setEnabled(False)
        self.actionSave_as_PDF.setEnabled(False)
        self.pushButton.setEnabled(False)
        for i in range(10):
            self.slider_list[i].setEnabled(False)   
        self.spectro_minimum_slider.setEnabled(False)
        self.spectro_maximum_slider.setEnabled(False)
        


     ########function to plot spectrogram####################
    def spectro(self):
        
        if self.signals[self.current_tab_index] != 0:
            if self.spectro_flag[self.current_tab_index] ==0 :
                self.spectro_widgets[self.current_tab_index].show()
                self.spectro_flag[self.current_tab_index] = 1
            else:
                self.spectro_widgets[self.current_tab_index].hide()
                self.spectro_flag[self.current_tab_index] = 0

    def spectro_sliders(self):
        self.spectro_minimum_slider.setValue(0)
        self.spectro_maximum_slider.setValue(100)
        self.spectro_min[self.current_tab_index]  = 0.0
        self.spectro_max[self.current_tab_index]  = 1.0

    def plot_spectro(self , output_signal ,color):
        fs = self.freq_sampling[self.current_tab_index] ####sampling frequency
        self.f,self.t,self.Sxx = signal.spectrogram(output_signal,fs)
        self.spectro_widgets[self.current_tab_index].clear()
        pg.setConfigOptions(imageAxisOrder='row-major')

        self.img= pg.ImageItem()
        self.spectro_widgets[self.current_tab_index].addItem(self.img)
        # Add a histogram to control the gradient of the image
        self.hist = pg.HistogramLUTItem()
        # Link the histogram to the image
        self.hist.setImageItem(self.img)
        # Fit the min and max levels of the histogram
        self.hist.setLevels(np.min(self.Sxx), np.max(self.Sxx))

        self.hist.gradient.restoreState(
                {'mode': 'rgb',
                'ticks': color})
        self.img.setImage(self.Sxx)

        self.img.scale(self.t[-1]/np.size(self.Sxx, axis=1),  self.f[-1]/np.size(self.Sxx, axis=0))

        self.spectro_widgets[self.current_tab_index].setXRange(0 , self.t[-1] , padding=0)
        self.spectro_widgets[self.current_tab_index].setYRange(0 ,  self.f[-1] , padding=0)

        self.spectro_widgets[self.current_tab_index].setLimits(xMin=0, xMax=self.t[-1], yMin= 0 , yMax= self.f[-1])
        # Add labels to the axis
        self.spectro_widgets[self.current_tab_index].setLabel('bottom', "Time", units='s')
            
        self.spectro_widgets[self.current_tab_index].setLabel('left', "Frequency", units='Hz')

    def update_spectro(self):
        self.spectro_min[self.current_tab_index] = float(self.spectro_minimum_slider.value())/100
        self.spectro_max[self.current_tab_index] = float(self.spectro_maximum_slider.value())/100
        self.spectro_minimum_slider.setMaximum(self.spectro_maximum_slider.value()) ## the maximum slider cant be higher than the min slider
        self.spectro_maximum_slider.setMinimum(self.spectro_minimum_slider.value())
        spectro_values = spectro_range(self.output_signal[self.current_tab_index] , self.spectro_min[self.current_tab_index] , self.spectro_max[self.current_tab_index])
        self.plot_spectro(spectro_values , self.color[self.current_color[self.current_tab_index]])
        self.spectro_widgets[self.current_tab_index].setYRange(self.f[-1] * self.spectro_min[self.current_tab_index] ,  self.f[-1] * self.spectro_max[self.current_tab_index] , padding=0)
    #####function for color palette
    def color_palette(self, i):
        self.plot_spectro(self.output_signal[self.current_tab_index] , self.color[i])
        self.current_color[self.current_tab_index] = i

    ##################################################################
   
    
    ##function to show about in popup message
    def pop_up(self):
        msg = QMessageBox()
        msg.setWindowTitle("About...")
        msg.setText('Signalviewer Version 1.0')
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setInformativeText('Copyright (C) 2021 SBME cairo university')
        

    ########function to show and hide the toolbar#####
    def toggle_tool(self, action):

        if action:
            self.toolBar.show()
        else:
            self.toolBar.hide()

    ########function to show and hide the status bar#####
    def toggle_status(self, action):

        if action:
            self.statusbar.show()
        else:
            self.statusbar.hide()
            
    #2nd comment: code repitition
    ######functionts for zoomig in and out0
    def zoom(self , factor):
        self.input_graph[self.current_tab_index].plotItem.getViewBox().scaleBy((factor, factor))
        self.output_graph[self.current_tab_index].plotItem.getViewBox().scaleBy((factor, factor))

    # def zoom_out(self):
    #     self.graphs_widgets[self.current_tab_index].plotItem.getViewBox().scaleBy((1.25,1.25))
    #     self.graphs_widgets[self.current_tab_index + 3].plotItem.getViewBox().scaleBy((1.25,1.25))
    
    #2nd comment: code repitition
    ######functionts for scrolling
    def scroll_x(self , sign):
        x_range = self.input_graph[self.current_tab_index].getViewBox().state['viewRange'][0] # the visible range in x axis
        rx = 0.1 * (x_range[1] - x_range[0]) * sign
        self.input_graph[self.current_tab_index].setXRange((x_range[0]+rx),(x_range[1]+rx) , padding=0)
        self.output_graph[self.current_tab_index].setXRange((x_range[0]+rx),(x_range[1]+rx) , padding=0)

    # def scroll_left(self):
    #     x_range = self.graphs_widgets[self.current_tab_index].getViewBox().state['viewRange'][0] # the visible range in x axis
    #     rx = 0.1 * (x_range[1] - x_range[0])
    #     self.graphs_widgets[self.current_tab_index].setXRange((x_range[0]-rx),(x_range[1]-rx) , padding=0)
    #     self.graphs_widgets[self.current_tab_index + 3].setXRange((x_range[0]-rx),(x_range[1]-rx) , padding=0)
    
    #2nd comment: code repitition
    def scroll_y(self , sign):
        y_range = self.input_graph[self.current_tab_index].getViewBox().state['viewRange'][1] # the visible range in y axis
        ry = 0.1 * (y_range[1] - y_range[0]) * sign
        self.input_graph[self.current_tab_index].setYRange((y_range[0]+ry),(y_range[1]+ry) , padding=0)

        y_range = self.output_graph[self.current_tab_index].getViewBox().state['viewRange'][1] # the visible range in y axis
        ry = 0.1 * (y_range[1] - y_range[0]) * sign
        self.output_graph[self.current_tab_index].setYRange((y_range[0]+ry),(y_range[1]+ry) , padding=0)
    
    # def scroll_down(self):
    #     y_range = self.graphs_widgets[self.current_tab_index].getViewBox().state['viewRange'][1] # the visible range in x axis
    #     ry = 0.1 * (y_range[1] - y_range[0])
    #     self.graphs_widgets[self.current_tab_index].setYRange((y_range[0]-ry),(y_range[1]-ry) , padding=0)

    #     y_range = self.graphs_widgets[self.current_tab_index + 3].getViewBox().state['viewRange'][1] # the visible range in x axis
    #     ry = 0.1 * (y_range[1] - y_range[0])
    #     self.graphs_widgets[self.current_tab_index + 3].setYRange((y_range[0]-ry),(y_range[1]-ry) , padding=0)
    ###function to adjust plot widget automatically 
    
    def reset_widget(self):
        self.input_graph[self.current_tab_index].clear()
        self.input_graph[self.current_tab_index].setLabel('bottom', "Time (ms)")
        self.output_graph[self.current_tab_index].clear()
        self.output_graph[self.current_tab_index].setLabel('bottom', "Time (ms)")
        self.spectro_widgets[self.current_tab_index].clear()
        self.spectro_widgets[self.current_tab_index].hide()
        self.spectro_flag[self.current_tab_index] = 0
        
        
            
    #####function to adjust automatically y axis range after zooming , scrolling 
    def limits(self ,widget,data):

        widget.setYRange(np.float(min(data)),np.float(max(data)) , padding=0)
        widget.setLimits(xMin=0, xMax=(len(data) - 1), yMin=np.float(min(data)), yMax=np.float(max(data)))
        

    ########configuration of plot widgets#####    
    def widget_configuration(self,widget,title):
        widget.showGrid(True, True, alpha=0.8)
        widget.setBackground('w') 
        widget.addLegend()
        widget.setTitle(title)
        widget.setXRange(0, 5000, padding=0)
    
    def export_pdf (self):
        
        fn, _ = QFileDialog.getSaveFileName(self, 'Export PDF', None, 'PDF files (.pdf);;All Files()')
        if fn != '':
            if QFileInfo(fn).suffix() == "" :
                fn += '.pdf'
        

            if self.input_graph[self.current_tab_index].scene():
                # export all items in all viewers as images
                input_signal_img = pg.exporters.ImageExporter(self.input_graph[self.current_tab_index].scene())
                input_signal_img.export('input_signal.png')
    
                outputSig_img = pg.exporters.ImageExporter(self.output_graph[self.current_tab_index].scene())
                outputSig_img.export('output_signal.png')
    
                #show spectrogram before printing
                self.spectro_widgets[self.current_tab_index].show()
                spectrogram_img = pg.exporters.ImageExporter(self.spectro_widgets[self.current_tab_index].scene())
                spectrogram_img.export('spectrogram.png')
                
                my_pdf = GeneratePDF(fn)
                my_pdf.create_pdf()
                my_pdf.save_pdf()
                if self.spectro_flag[self.current_tab_index] == 0 :
                    self.spectro_widgets[self.current_tab_index].hide()   

    def new_tab(self):
        self.tab["tab"+str(self.i)] = QtWidgets.QWidget()
        self.tab["tab"+str(self.i)].setObjectName("tab" + str(self.i))
        # plot("index" , self.tab["tab"+str(self.i)].getIndex())
        self.layout["gridLayout_new" + str(self.i)] = QtWidgets.QGridLayout(self.tab["tab"+str(self.i)])
        self.layout["gridLayout_new" + str(self.i)].setObjectName("gridLayout_new"+ str(self.i))
        
        self.layout["horizontalLayout_new" + str(self.i)] = QtWidgets.QHBoxLayout()
        self.layout["horizontalLayout_new" + str(self.i)].setObjectName("horizontalLayout_new"+ str(self.i))

        self.layout["verticalLayout_1new" + str(self.i)] = QtWidgets.QVBoxLayout()
        self.layout["verticalLayout_1new" + str(self.i)].setObjectName("verticalLayout_1new"+ str(self.i))

        self.input_graph.append(PlotWidget(self.tab["tab"+str(self.i)]))
        self.input_graph[-1].setObjectName("widget_before" + str(self.i))
        self.layout["verticalLayout_1new" + str(self.i)].addWidget(self.input_graph[-1])

        self.output_graph.append(PlotWidget(self.tab["tab"+str(self.i)]))
        self.output_graph[-1].setObjectName("widget_after" + str(self.i))
        self.layout["verticalLayout_1new" + str(self.i)].addWidget(self.output_graph[-1])

        self.layout["horizontalLayout_new" + str(self.i)].addLayout(self.layout["verticalLayout_1new" + str(self.i)])
        self.layout["verticalLayout_2new" + str(self.i)] = QtWidgets.QVBoxLayout()
        self.layout["verticalLayout_2new" + str(self.i)].setObjectName("verticalLayout_2new" + str(self.i))

        self.spectro_widgets.append(PlotWidget(self.tab["tab"+str(self.i)]))
        self.spectro_widgets[-1].setObjectName("widget_s" + str(self.i))
        self.layout["verticalLayout_2new" + str(self.i)].addWidget(self.spectro_widgets[-1])

        self.layout["horizontalLayout_new" + str(self.i)].addLayout(self.layout["verticalLayout_2new" + str(self.i)])
        self.layout["gridLayout_new" + str(self.i)].addLayout(self.layout["horizontalLayout_new" + str(self.i)], 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab["tab"+str(self.i)], "")

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab["tab"+str(self.i)]), " Signal " +str(self.i))
        self.widget_configuration(self.input_graph[-1] , "Input signal "+ str(self.i))
        self.widget_configuration(self.output_graph[-1] , "Output signal "+ str(self.i))
        self.widget_configuration(self.spectro_widgets[-1] , "Spectrogram " + str(self.i))
        self.spectro_widgets[-1].hide()

        self.current_color.append(0)
        self.spectro_flag.append(0) 
        self.signals.append(0) 
        self.file_name.append(0) 
        self.input_signal.append(0) 
        self.freq_sampling.append(0) 
        self.output_signal.append(0) 
        self.spectro_min.append(0)
        self.spectro_max.append(1)
        self.timer.append(0)
        self.interval.append(0)
        self.index.append(0)
        normal_gain = 10 * [1]
        self.gain.append(normal_gain)
        
        self.i += 1

        

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()