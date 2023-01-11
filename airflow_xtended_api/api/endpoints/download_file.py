import logging
import os
import socket

from flask import request, send_file
from airflow import settings
from airflow.api_connexion import security
from airflow.security import permissions
from airflow.www.app import csrf

from airflow_xtended_api.api.app import blueprint
import airflow_xtended_api.utils as utils
import airflow_xtended_api.api.dag_utils as dag_utils
from airflow_xtended_api.api.response import ApiResponse


@blueprint.route("/download_file", methods=["POST"])
@csrf.exempt
@security.requires_access([])
def download_file():
    """Custom Function for the download_file API.
    Download files from the specified path.
    """
    logging.info("Executing custom 'download_file' function")

    # check if the post request has the file part
    if (
        not request.form.get("filename")
    ):
        logging.warning("The file argument wasn't provided")
        return ApiResponse.bad_request("file should be provided")
    filename = request.form.get("filename")
    path = request.form.get("path")
    if path is None:
        path = dag_utils.get_dag_folder()


    # save file
    file_path = os.path.join(path, filename)

    # Check if the file already exists.
    if not os.path.isfile(file_path):
        logging.warning("File to download does not exist")
        hostname = socket.gethostname()
        return ApiResponse.not_found(
            f"The file {file_path} does not exist on host {hostname}"
        )



    return send_file(file_path)
