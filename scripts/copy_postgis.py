import shutil
import os

from arches_lintels.models.dependencies.postgres import PostgresModel

#TODO: Since scripts/ isn't in the lintels dir, we should call this in the psql model 
# via calling the app with -dev 

def copy_postgis():
    postgres_model = PostgresModel()
    postgres_path = postgres_model.postgres_path
    postgis_path = postgres_model.postgis_path
    
    shutil.copytree(
        os.path.join(postgis_path, "bin"), 
        os.path.join(postgres_path, "bin"), 
        dirs_exist_ok=True
    )
    shutil.copytree(
        os.path.join(postgis_path, "lib"), 
        os.path.join(postgres_path, "lib"), 
        dirs_exist_ok=True
    )
    shutil.copytree(
        os.path.join(postgis_path, "share"), 
        os.path.join(postgres_path, "share"), 
        dirs_exist_ok=True
    )

    print("Copy of PostGIS bin, lib, share dirs complete")