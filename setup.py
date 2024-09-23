config_content = """
instances:
  radarr:
    - name: "Master"
      base_url: "http://localhost:7878"
      api_key: "API_KEY"
    - name: "DEV"
      base_url: "http://localhost:7887"
      api_key: "API_KEY"
  sonarr:
    - name: "Master"
      base_url: "http://localhost:8989"
      api_key: "API_KEY"
    - name: "DEV"
      base_url: "http://localhost:8998"
      api_key: "API_KEY"
settings:
  export_path: "./exports"
  import_path: "./imports"
  ansi_colors: true

"""

with open('config.yml', 'w') as file:
    file.write(config_content)
