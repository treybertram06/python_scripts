import epd2in13_V2
from PIL import Image,ImageDraw,ImageFont

try:
    # Initialize the display
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    # Create a new image with the display dimensions
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)

    # Set the font and size
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)

    # Draw the text on the image
    draw.text((10, 0), 'Hello, World!', font = font, fill = 0)

    # Display the image on the e-paper display
    epd.display(epd.getbuffer(image))
    time.sleep(2)

except IOError as e:
    print(e)

except KeyboardInterrupt:    
    print("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()