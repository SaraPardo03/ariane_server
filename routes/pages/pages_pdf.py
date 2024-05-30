from fpdf import FPDF

base_url = "http://127.0.0.1:8080/"

class pages_pdf(FPDF):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
  """def header(self):
    # Select Arial bold 15
    self.set_font('Times', 'B', 15)
    # Move to the right
    self.cell(80)
    # Framed title
    self.cell(30, 10, 'Title', 1, 0, 'C')
    # Line break
    self.ln(20)"""

  def footer(self):
    # Go to 1.5 cm from bottom
    self.set_y(-15)
    # Select Arial italic 8
    self.set_font('Times', 'I', 10)
    # Print centered page number
    #self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'R')
  
  def draw_story_title(self, story):
    self.add_page()

    if story.cover:
      image_url = f"{base_url}{story.cover}"
      self.image(image_url, x=0, y=0, w=self.w, h=self.h)
      
    self.add_page()
    #Author
    self.ln(24)
    self.set_font('Times', '', 18)
    self.cell(0, h = 6, txt = self.author, border = 0, ln = 0, align = 'C', fill = False, link = '')
    #Title
    self.ln(12)
    self.set_font('Times', 'B', 24)
    self.cell(0, h = 6, txt = self.title, border = 0, ln = 0, align = 'C', fill = False, link = '')
    #Summary
    self.ln(24)
    self.set_font('Times', 'B', 14)
    self.cell(0, h = 6, txt = "Résumer", border = 0, ln = 0, align = 'C', fill = False, link = '')
    self.ln(12)
    self.set_font('Times', '', 13)
    self.multi_cell( w = 0, h=  6, txt = self.subject, border = 0, align = 'J', fill = False)
    self.add_page()

  def draw_page(self, pages, page) -> None:
    if page.first:
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
    #Page text
    self.ln(6)
    self.set_font('Times', '', 14)
    self.multi_cell( w = 0, h=  6, txt = text, border = 0, align = 'J', fill = False)

    self.draw_choices(pages, page.choices)
  
  def draw_pages(self, pages):
    def get_title_len(page):
      return page.title
    
    pages.sort(key=get_title_len)
    for page in pages:
      if not page.first:
        self.draw_page(pages, page)      
  
  def draw_choice(self, pages, choice):
    title = choice.title.replace('’', "'")
    section = [page.section for page in pages if page.id == choice.send_to_page_id]
    section = str(section[0])
    #Page text
    self.ln(12)
    self.set_font('Times', 'I', 14)
    self.multi_cell( w =0, h=  6, txt = title , border = 0, align = 'L', fill = False)
    self.ln(3)
    self.set_font('Arial', 'B', 10)
    self.cell(0, 6, "Rendez-vous à la section n° " + section, border=0, align='R', fill=False)

  def draw_next_pages(self, pages, previous_pages):
    if previous_pages:
      # List of previous page ids 
      previous_page_ids = [previous_page.id for previous_page in previous_pages]
      # List of next page to draw
      next_pages = [next_page for next_page in pages if next_page.previous_page_id in previous_page_ids]
      lenght = len(next_pages)
      if lenght > 0:
        for next_page in next_pages:
          self.draw_page(pages, next_page)

        self.draw_next_pages(pages, next_pages) 
  
  def draw_choices(self, pages, choices):
    if choices:
      lenght = len(choices)
      if lenght > 0:
        for choice in choices:
          self.draw_choice(pages, choice)

  def get_section(self, story, first_page, pages):
    section = pages_pdf(orientation = 'P', unit = 'mm', format='A5')
    section.set_title(story.title)
    section.set_author('Artist Unknown')
    section.set_subject(story.summary)
    
    section.draw_story_title(story)
    section.draw_page(pages, first_page)
    section.draw_pages(pages)