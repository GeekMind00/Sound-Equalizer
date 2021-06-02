from reportlab.pdfgen import canvas
import os
class GeneratePDF():

    
    def __init__(self, filename):
        super().__init__()
    # Content for PDF
        self.fileName = filename
        self.documentTitle = 'Equalizer'
        self.title = 'Equalizer'

        # Signals imgs used in generating PDF
        self.input_signal = 'input_signal.png'
        self.output_signal = 'output_signal.png'
        self.spectrogram = 'spectrogram.png'

        #  Create document with content given
        
        self.pdf = canvas.Canvas(self.fileName)
        self.pdf.setTitle(self.documentTitle)

        #  Adjusting title

        self.pdf.setFont('Courier-Bold', 36)
        self.pdf.drawCentredString(315, 750, 'Equalizer report')

        #  Adjusting sub-title
        self.pdf.setFont('Courier-Bold', 12)
        

        #  Draw all lines for the table
        self.pdf.line(10, 700, 570, 700)
        self.pdf.line(10, 500, 570, 500)
        self.pdf.line(10, 300, 570, 300)

        self.pdf.line(110, 100, 110, 700)
        

    #ruler for alignment
    def drawMyRuler(self):
        self.pdf.drawString(100, 810, 'x100')
        self.pdf.drawString(200, 810, 'x200')
        self.pdf.drawString(300, 810, 'x300')
        self.pdf.drawString(400, 810, 'x400')
        self.pdf.drawString(500, 810, 'x500')

        self.pdf.drawString(10, 100, 'y100')
        self.pdf.drawString(10, 200, 'y200')
        self.pdf.drawString(10, 300, 'y300')
        self.pdf.drawString(10, 400, 'y400')
        self.pdf.drawString(10, 500, 'y500')
        self.pdf.drawString(10, 600, 'y600')
        self.pdf.drawString(10, 700, 'y700')
        self.pdf.drawString(10, 800, 'y800')

# Plotting the signals names
    def sigName(self, signal1, signal2 ,signal3):
        self.pdf.drawString(10, 600, signal1)
        self.pdf.drawString(10, 400, signal2)
        self.pdf.drawString(10, 200, signal3)

# Sending all signals images to their positions in the table
    def sigImage(self, img1, img2):
        self.pdf.drawInlineImage(img1, 120, 515, width=410,
                                 height=170, preserveAspectRatio=False, showBoundary=True)
        self.pdf.drawInlineImage(img2, 120, 315, width=410,
                                 height=170, preserveAspectRatio=False, showBoundary=True)



# Sending all signals spectroimages to their positions in the table
    def spectroImage(self, img2):
        self.pdf.drawInlineImage(img2, 120, 115, width=410,
                                 height=170, preserveAspectRatio=False, showBoundary=True)

    # Generating the PDF
    def create_pdf(self):
        self.sigName('Input Signal', 'Output Signal', 'Spectrogram') #reduce font size 
        self.sigImage(self.input_signal, self.output_signal)
        self.spectroImage(self.spectrogram)
        #self.drawMyRuler()
        #self.save_pdf()

    def save_pdf(self):
        self.pdf.save()
        
        # delete created images after generating PDF file 
        if os.path.exists(self.fileName): #11111
            os.remove("input_signal.png")
            os.remove("output_signal.png")
            os.remove("spectrogram.png")


#To run the code:
# test = GeneratePDF()
# test.create_pdf()
