python-pip:
  pkg:
    - installed

virtualenvwrapper:
  pip.installed:
    - require:
      - pkg: python-pip
