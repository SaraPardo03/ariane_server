from fpdf import FPDF
from PIL import Image

base_url = "http://127.0.0.1:8080/"

class pages_pdf(FPDF):
  def __init__(self, *args, **kwargs):
    """
      Initialize the PDF with given arguments and set the page dimensions to A5.

      Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """
    super().__init__(*args, **kwargs)
    # Définir les dimensions de la page A5
    self.page_width = 148  # Largeur en mm
    self.page_height = 210

  def draw_cover_title(self, story):
    """
      Draw the cover title of the story.

      Args:
        story: The story object containing cover information.
    """
    if story.cover:
      image_url = f"{base_url}{story.cover}"
      self.image(image_url, x=0, y=20, w=self.w, h=self.h -20)

  def draw_story_title(self, title_color):
    """
      Draw the story title with the specified color.

      Args:
        title_color (list): List of RGB values for the title color.
    """
    self.set_font('Times', '', 22)
    self.set_fill_color(43, 45, 49)
    self.set_text_color(255, 255, 255) 
    self.set_xy(0, 0)
    self.cell(self.page_width, h = 10, txt = "UN LIVRE DONT VOUS ETES LE HEROS", border = 0, ln = True, align = 'C', fill = True, link = '')
    #Author
    self.set_xy(0, 10)
    self.set_fill_color(255, 191, 0)
    self.set_text_color(0, 0, 0)
    self.set_font('Times', '', 18)
    self.cell(self.page_width, h = 10, txt = self.author, border = 0, ln = True, align = 'C', fill = True, link = '')
    #Title
    self.ln(12)
    self.set_text_color(int(title_color[0]),int(title_color[1]), int(title_color[2])) 
    self.set_font('Times', 'B', 34)
    self.multi_cell(0, h = 6, txt = self.title, border = 0, align = 'C', fill = False)
    self.set_text_color(0, 0, 0) 

  def draw_summary(self):
    """
      Draw the summary page of the story.
    """
    self.add_page()
    self.ln(24)
    self.set_font('Times', 'B', 14)
    self.cell(0, h = 6, txt = "Résumer", border = 0, ln = 0, align = 'C', fill = False, link = '')
    self.ln(12)
    self.set_font('Times', '', 13)
    self.multi_cell( w = 0, h=  6, txt = self.subject, border = 0, align = 'J', fill = False)

  def draw_page(self, pages, page) -> None:
    """
      Draw an individual page of the story.

      Args:
        pages (list): List of all pages.
        page: The page object to draw.
    """
    if page.first:
      self.add_page()
      title = "Prologue"
    else:
      if page.choice_title != "":
        title = page.choice_title
      else:
        title = page.title

    section =""
    if page.section != None and page.section != 0:
      section = str(page.section)

    title = title.replace('’', "'") 
    text = page.text.replace('’', "'")
    
    if not page.first:
      self.ln(24)
    if self.get_y() > 150:
      self.add_page()
    
    #Page title
    self.set_font('Times', 'B', 15)
    self.multi_cell(0, h = 8, txt = section, border = 0, align = 'C', fill = False)
    self.ln(3)
    #Page title
    self.set_font('Times', 'I', 16)
    self.multi_cell(0, h = 8, txt = title, border = 0, align = 'C', fill = False)
    
    #Image
    if page.image != "" and page.image != None:
      # open image with Pillow to get dimension
      image_page_path = f"./{page.image}"
      with Image.open(image_page_path) as img:
        img_width, img_height = img.size

      max_width = self.page_width - 28 # Maximum width for the image

      # Calculate x position to center image horizontally
      x = (self.page_width - max_width) / 2
      y = self.get_y() # Position y in mm from the top left corner
      
      # Calculate the new height to maintain the ratio
      ratio = max_width / img_width
      new_height = img_height * ratio

      if self.page_height - y  < new_height:
        self.add_page()
        y = self.get_y() + 10
      else:
        self.ln(3)
        
      image_page_url = f"{base_url}{page.image}"

      self.image(image_page_url, x=x, y=y, w=max_width, h=new_height)
      text_y_position = y + new_height + 10  # add 10 mm after image
      self.set_xy(10, text_y_position) 

    #Page text
    self.ln(6)
    self.set_font('Times', '', 14)
    self.multi_cell( w = 0, h=  6, txt = text, border = 0, align = 'J', fill = False)

    if len(page.choices) == 0:
      self.ln(6)
      self.cell(w=0, h=6, txt="Fin", border = 0, ln = True, align = 'C', fill = False, link = '')
    else:
      self.draw_choices(pages, page.choices)
  
  def draw_pages(self, pages):
    """
      Draw all pages.

      Args:
        pages (list): List of all pages.
    """
    for page in pages:
      if not page.first:
        self.draw_page(pages, page)      
  
  def draw_choice(self, pages, choice):
    """
      Draw a choice on the page.

      Args:
        pages (list): List of all pages.
        choice: The choice object to draw.
    """
    title = choice.title.replace('’', "'")
    section = [page.section for page in pages if page.id == choice.send_to_page_id]
    section = str(section[0])
    #Page text
    self.ln(12)
    self.set_font('Times', 'I', 14)
    self.multi_cell( w =0, h=  6, txt = title , border = 0, align = 'L', fill = False)
    self.ln(1)
    self.set_font('Arial', 'B', 10)
    self.cell(0, 6, "Rendez-vous à la section n° " + section, border=0, align='R', fill=False)
  
  def draw_choices(self, pages, choices):
    """
      Draw all choices for a page.

      Args:
        pages (list): List of all pages.
        choices (list): List of choices to draw.
    """
    if choices:
      lenght = len(choices)
      if lenght > 0:
        for choice in choices:
          self.draw_choice(pages, choice)
  
  def draw_aventure_pages(self):
    """
      Draw the adventure pages.
    """
    self.add_page()
    image_url = f"{base_url}static/page_aventure.png"
    self.image(image_url, x=0, y=0, w=self.page_width, h=self.page_height)
    self.add_page()
    image_url = f"{base_url}static/page_aventure_2.png"
    self.image(image_url, x=0, y=0, w=self.page_width, h=self.page_height)
