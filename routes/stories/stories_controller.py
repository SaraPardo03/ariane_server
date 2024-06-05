import os
import sys
# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import io
import base64
import zipfile
import json

from flask.views import MethodView
from flask import jsonify, send_file, request
from flask_smorest import Blueprint


from utils.jwt_decorator import jwt_required

from .stories_service import stories_service
from routes.pages.pages_service import pages_service
from routes.choices.choices_service import choices_service

from .dto.request.story_create import create_story
from .dto.request.story_update import update_story
from .dto.response.story_response import story_response, stories_response

from .story_mapper import to_dict, to_entity
from routes.pages.page_mapper import to_entity as page_to_entity
from routes.pages.page_mapper import to_dict as page_to_dict
from routes.choices.choice_mapper import to_entity as choice_to_entity
from routes.choices.choice_mapper import to_dict as choice_to_dict

# Initialize services
stories_service = stories_service()
pages_service = pages_service()
choices_service = choices_service()

stories = Blueprint("stories", "stories", url_prefix="/stories", description="stories routes")
 
@stories.route("/<user_id>")
class stories_controller(MethodView):
  """
    Controller class for managing stories.

    This controller provides endpoints for retrieving, creating, updating, and deleting stories.
  """
  @stories.response(200, stories_response)
  @jwt_required
  def get(self, user_id:str):
    """
      Retrieve all stories associated with a user.

      Args:
          user_id (str): The identifier of the user whose stories are to be retrieved.

      Returns:
          dict: A dictionary containing the list of stories associated with the specified user.
      
      Raises:
          Exception: If an error occurs while retrieving the stories.
    """
    try:
      stories = stories_service.get_all(user_id)
      stories = [to_dict(story) for story in stories]
      return {"stories": stories}
    except Exception as e:
      return jsonify({"error": str(e)}), 500
      
  @stories.arguments(create_story)
  @stories.response(201, story_response)
  @jwt_required
  def post(self, story_data:dict, user_id:str):
    """
      Create a new story for a user.

      Args:
          story_data (dict): The data for the new story.
          user_id (str): The identifier of the user for whom the story is created.

      Returns:
          dict: A dictionary containing the created story.
      
      Raises:
          ValueError: If the provided data is invalid.
          Exception: If an error occurs while creating the story.
    """
    try:
      story = stories_service.create_story(to_entity(story_data))
    except ValueError as ve:
      return jsonify({"error": str(ve)}), 400
    except Exception as e:
      return jsonify({"error": str(e)}), 500
  
    return jsonify({"story": to_dict(story)})

  @stories.route("/<user_id>/<story_id>")
  class story_controller(MethodView):
    """
      Controller class for managing individual stories.
    """
    @stories.response(200, story_response)
    @jwt_required
    def get(self, story_id:str, user_id:str,):
      """
        Retrieve a story by its identifier.

        Args:
            story_id (str): The identifier of the story to retrieve.
            user_id (str): The identifier of the user who owns the story.

        Returns:
            dict: A dictionary containing the retrieved story.
        
        Raises:
            ValueError: If no story is found with the specified identifier.
            Exception: If an error occurs while retrieving the story.
      """
      try:
          story = stories_service.get_story_by_id(story_id)
          return jsonify({"story": to_dict(story)})
      except ValueError as ve:
          return jsonify({"error": str(ve)}), 404
      except Exception as e:
          return jsonify({"error": str(e)}), 500
      
    @stories.arguments(update_story)
    @stories.response(200, story_response)
    @jwt_required
    def put(self, story_data:dict, story_id:str, user_id:str,):
      """
        Update a story by its identifier.

        Args:
            story_data (dict): The updated data for the story.
            story_id (str): The identifier of the story to update.
            user_id (str): The identifier of the user who owns the story.

        Returns:
            dict: A dictionary containing the updated story.
        
        Raises:
            ValueError: If no story is found with the specified identifier or the provided data is invalid.
            Exception: If an error occurs while updating the story.
        """
      image_base64 = story_data.get('cover')

      # Decode the cover image and save it to the server
      image_url = None
      if image_base64:
        image_data = base64.b64decode(image_base64.split(',')[1])
        image_filename = f"{story_id}.png"
        image_path = os.path.join('static', 'images', image_filename)
        with open(image_path, 'wb') as f:
          f.write(image_data)
        image_url = f"/static/images/{image_filename}"
      
      story_data['cover'] = image_url
      try:
        updated_story = stories_service.update_story(story_id, story_data)
        return jsonify({"story": to_dict(updated_story)})
      except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
      except Exception as e:
        return jsonify({"error": str(e)}), 500
      
    @stories.response(status_code=200)
    @jwt_required
    def delete(self, story_id:str, user_id:str,):
      """
        Delete a story by its identifier.

        Args:
            story_id (str): The identifier of the story to delete.
            user_id (str): The identifier of the user who owns the story.

        Returns:
            dict: A dictionary containing a success message if the story is deleted successfully.
        
        Raises:
            ValueError: If no story is found with the specified identifier.
            Exception: If an error occurs while deleting the story.
        """
      try:
        success = stories_service.delete_story(story_id)
        if not success:
            return jsonify({"error": "Story not found"}), 404
        return jsonify({"message": "Story successfully deleted"}), 200
      except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
      except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    @stories.route('/upload_story/<story_id>', methods=['POST'])
    def upload_story(story_id):
      """
        Upload a story as a zip file.

        Args:
            story_id (str): The identifier of the story to upload.

        Returns:
            Flask response: A zip file containing the story and its assets.
        
        Raises:
            ValueError: If no story is found with the specified identifier.
            Exception: If an error occurs while creating the zip file.
      """
      try:
        memory_file = io.BytesIO()

        with zipfile.ZipFile(memory_file, 'w') as zf:
          story = stories_service.get_full_story_by_id(story_id)
          if not story:
            raise ValueError('Story not found')
            
          # Add story data to the zip
          story_data = json.dumps(to_dict(story), default=str)
          zf.writestr('story.json', story_data)
          
          # Add story cover to the zip
          if story.cover != None and story.cover != "":
            cover_path = "." + story.cover
            if os.path.exists(cover_path):
              zf.write(cover_path, arcname=f"{story.cover}")

          # Add page images to the zip
          for page in story.pages:
            if page.image != None and page.image != "":
              image_path = "." + page.image
              if os.path.exists(image_path):
                zf.write(image_path, arcname=f"{page.image}")

        memory_file.seek(0)

        return send_file(
          memory_file,
          mimetype='application/zip',
          as_attachment=True,
          download_name=f'story_{story_id}.ariane'
        )
      except ValueError as e:
        return jsonify({"error": str(e)}), 404
      except Exception as e:
        return jsonify({"error": "An error occurred while creating the ZIP file"}), 500
    
    @stories.route('/import_story', methods=['POST'])
    def import_story():
      """
        Import a story from a zip file.

        Returns:
            dict: A success message if the story is imported successfully.
        
        Raises:
            ValueError: If no story is found in the zip file.
            Exception: If an error occurs while importing the story.
      """
      if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
      
      file = request.files['file']
      if file and file.filename.endswith('.ariane'):
        try:
          memory_file = io.BytesIO(file.read())

          with zipfile.ZipFile(memory_file, 'r') as zf:
            story_data = zf.read('story.json')
            story_dict = json.loads(story_data)

            story = stories_service.create_story(to_entity(story_dict))

            if story.cover:
              cover_path = '/'.join(story_dict["cover"].split('/')[1:-1])
              cover_filename = story_dict["cover"].split('/')[-1]
              cover_extension = cover_filename.split('.')[1]

              try:
                # Lire l'image de l'archive
                image_data = zf.read(f'{cover_path}/{cover_filename}')
                
                # Déterminer le nouveau nom de fichier
                new_cover_filename = f"{story.id}.{cover_extension}"

                # Déterminer le chemin du nouveau fichier
                new_cover_path = f'{cover_path}/{new_cover_filename}'

                # Sauvegarder l'image renommée
                with open(new_cover_path, 'wb') as image_file:
                  image_file.write(image_data)

                # Mettre à jour la référence de l'image dans l'objet story
                story.cover = f'/{new_cover_path}'
                stories_service.update_story(story.id, to_dict(story))
              except KeyError:
                print(f"Image {cover_filename} not found in the archive")

            if "pages" in story_dict and story_dict["pages"]:
              pages = [page for page in story_dict["pages"]]
              first_page = next((page for page in pages if page["first"]), None)

              def save_next_page(current_page):
                if current_page:
                  current_page["storyId"] = story.id
                  choices = current_page.get("choices", [])
                  current_page.pop("choices")
                
                  page = pages_service.create_page(page_to_entity(current_page))
                  if page.image:
                    image_path = '/'.join(page.image.split('/')[1:-1])
                    image_filename = page.image.split('/')[-1]
                    image_extension = image_filename.split('.')[1]
                    try:
                      # Lire l'image de l'archive
                      image_data = zf.read(f'{image_path}/{image_filename}')
                      
                      # Déterminer le nouveau nom de fichier
                      new_image_filename = f"{page.id}.{image_extension}"

                      # Déterminer le chemin du nouveau fichier
                      new_image_path = f'{image_path}/{new_image_filename}'

                      # Sauvegarder l'image renommée
                      with open(new_image_path, 'wb') as image_file:
                        image_file.write(image_data)

                      # Mettre à jour la référence de l'image dans l'objet story
                      page.image = f'/{new_image_path}'
                      pages_service.update_page(page.id, page_to_dict(page))
                    except KeyError:
                      print(f"Image {image_filename} not found in the archive")
                    
                  if len(choices) > 0:
                    for current_choice in choices:
                      send_to_page = next((page for page in pages if page["id"] == current_choice["sendToPageId"]), None)
                      if send_to_page:
                        send_to_page["storyId"] = story.id
                        send_to_page["previousPageId"] = page.id

                        next_page = save_next_page(send_to_page)
                        if next_page:
                          current_choice["pageId"] = page.id
                          current_choice["sendToPageId"] = next_page.id
                          try:
                            choices_service.create_choice(choice_to_entity(current_choice))
                          except TypeError as e:
                            print(f"Error creating choice: {e}")
                  return page
              save_next_page(first_page)
          return jsonify({"message": "Story imported successfully"}), 200
        except ValueError as ve:
          return jsonify({"error": str(ve)}), 400
        except Exception as e:
          return jsonify({"error": str(e)}), 500

      return jsonify({"error": "Invalid file format"}), 400
      