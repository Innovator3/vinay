from django.shortcuts import render, redirect
from .models import User
from django.http import JsonResponse, HttpResponse
from .tests import (
    input_image_setup,
    get_gemini_response,
    extract_pdf_text,
    dymanic_path,
    delete_all_files,
)
from django.views.decorators.csrf import csrf_exempt
import json
from PIL import Image
import os

# Create your views here.


def loginUser(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(uname=username)
            print(user, user.password)
            if user is not None and user.password == password:
                request.session["username"] = username

                return redirect("upload")
        except Exception as e:
            print(str(e))
            print("User does not exist")

    return render(request, "login.html")


def uploadFile(request):
    username = request.session.get("username", None)
    print(delete_all_files(dymanic_path("staticfiles")))
    delete_all_files(dymanic_path("static", "images"))
    delete_all_files(dymanic_path("static"))
    processed = False
    if request.method == "POST" and request.FILES["file"]:
        uploaded_file = request.FILES["file"]
        print("vinay---filename---", uploaded_file.name)
        if uploaded_file.name.endswith(".pdf"):
            ocr_content = extract_pdf_text(uploaded_file.read())
            image_data = None
            processed = True
            with open(dymanic_path("staticfiles", "ocr_extracted.txt"), "w") as f:
                f.write(ocr_content)

        else:
            image_data = input_image_setup(uploaded_file)
            img = Image.open(uploaded_file)
            img.save(
                dymanic_path("static", "images", f"_{1}.jpeg"), "JPEG", quality=100
            )
            ocr_content = None
            processed = True

        response = get_gemini_response(image_data=image_data, ocr_content=ocr_content)
        # print("response.text", response)
        with open(dymanic_path("staticfiles", "genai_extracted.json"), "w") as f:
            json.dump(response, f)

        return render(
            request,
            "index.html",
            {
                "username": username,
                "processed": processed,
                "file_name": uploaded_file.name,
            },
        )
    return render(
        request,
        "index.html",
        {
            "username": username,
        },
    )


def get_fields_data():
    with open(dymanic_path("staticfiles", "genai_extracted.json"), "r") as f:
        # json_bytes = json.loads(f)
        # print("genai_extracted.json", f)
        json_bytes = (
            f.read()
            .replace("\\n", "")
            .replace("JSON", "")
            .replace("```", "")
            .replace("\\", "")
            .replace("json", "")
            .replace("Not found in the document", "")[1:-1]
        )
        print("input data ----------------", json_bytes)
    input_data = dict(json.loads(json_bytes))
    field_values_dict = {}

    def process_dict(data, prefix=""):
        for key, value in data.items():
            if isinstance(value, dict):
                process_dict(value, prefix + key)
            else:
                result_key = f"{prefix}{key}"
                if "Confidence" not in result_key:
                    result_value = [
                        value,
                        int(data.get(f"{key}Confidence", "0") * 100),
                    ]
                    field_values_dict[result_key] = result_value

    process_dict(input_data)
    return field_values_dict


def keyingscreen_view(request):
    field_dict = get_fields_data()
    image_urls = os.listdir(dymanic_path("static", "images"))
    print("image_urls", image_urls)
    file_name = request.GET.get("file_name")
    print("image_urls", file_name)
    return render(
        request,
        "keyingscreen.html",
        {
            "field_values_dict": field_dict,
            "image_urls": image_urls,
            "file_name": file_name,
        },
    )


@csrf_exempt
def save_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            filename = (
                data.get("filename", "default_filename.json").split(".")[0] + ".json"
            )
            form_data = data.get("formData", {})

            # Save the data to a JSON file
            print("vinay----------", filename)
            with open(dymanic_path("static", filename), "w") as json_file:
                json.dump(form_data, json_file)

            return JsonResponse({"status": "success"})

        except json.JSONDecodeError as e:
            return JsonResponse({"status": "success"})

    return JsonResponse({"status": "success"})


def download_view(request):
    file_name = request.GET.get("file_name").split(".")[0] + ".json"
    path = dymanic_path("static", file_name)

    if os.path.exists(path) and os.path.isfile(path):
        with open(path, "rb") as json_file:
            json_data = json_file.read()
            response = HttpResponse(json_data, content_type="application/json")
            response["Content-Disposition"] = (
                f'attachment; filename="{os.path.basename(path)}"'
            )
            return response
    else:
        return HttpResponse("File not found", status=404)
