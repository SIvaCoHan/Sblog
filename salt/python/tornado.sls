tornado:
  pip.installed:
    - name: tornado >= 4.0, <= 4.3
    - require:
      - pkg: python-pip
