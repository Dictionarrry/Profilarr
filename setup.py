import os
master_radarr_base_url = os.environ.get("MASTER_RADARR_BASEURL", "http://localhost:7878")
master_radarr_apikey = os.environ.get("MASTER_RADARR_APIKEY", "API_KEY")
dev_radarr_base_url = os.environ.get("DEV_RADARR_BASEURL", "http://localhost:7887")
dev_radarr_apikey = os.environ.get("DEV_RADARR_APIKEY", "API_KEY")
master_sonarr_base_url = os.environ.get("MASTER_SONARR_BASEURL", "http://localhost:8989")
master_sonarr_apikey = os.environ.get("MASTER_SONARR_APIKEY", "API_KEY")
dev_sonarr_base_url = os.environ.get("DEV_SONARR_BASEURL", "http://localhost:8998")
dev_sonarr_apikey = os.environ.get("DEV_SONARR_APIKEY", "API_KEY")
config_content = f"""
instances:
  radarr:
    - name: "Master"
      base_url: "{master_radarr_base_url}"
      api_key: "{master_radarr_apikey}"
    - name: "DEV"
      base_url: "{dev_radarr_base_url}"
      api_key: "{dev_radarr_apikey}"
  sonarr:
    - name: "Master"
      base_url: "{master_sonarr_base_url}"
      api_key: "{master_sonarr_apikey}"
    - name: "DEV"
      base_url: "{dev_sonarr_base_url}"
      api_key: "{dev_sonarr_apikey}"
settings:
  export_path: "./exports"
  import_path: "./imports"
  ansi_colors: true

"""

with open('config.yml', 'w') as file:
    file.write(config_content)
