from django.conf import settings
import os
from documentation.djconf import ignored_dir_chars, ignored_file_chars, ignored_apps
from documentation.structure import mini_text, sub_file_content, app_structure,\
    file_content, include_text


def configureSphinxSourceFile():



    
    
    app_text = ""
    #includes = ""
    doc_path = os.path.dirname(__file__)
    app_path = os.path.abspath(os.path.join(doc_path, ".."))
    src_path = os.path.join(doc_path, "gen")
    for app in [x for x in settings.INSTALLED_APPS if "django.contrib." not in x and x not in ignored_apps]:
        added_text = ""
        appDir = app_path
        for i in [ x for x in app.split(".")]:
            appDir = os.path.join(appDir,i)
            for a,b,c in os.walk(appDir):
                c.sort()
                for Zfile in c:
                    if ".py" in Zfile and not ".pyc" in Zfile and not ".pyo" in Zfile:
                        if not [j for j in ignored_dir_chars if j in a]:
                            if not [k for k in ignored_file_chars if k in Zfile]:
                                modName = Zfile.rpartition(".")[0]
                                modPath = "{}.{}".format(os.path.relpath(a, app_path).replace("/","."), modName)
                                added_text += mini_text.format(modName,modPath)
        text = sub_file_content.format(app.title(), added_text)
        f = open(os.path.join(src_path, "_source", "{}.rst".format(app.replace(".","_"))),'w')
        f.write(text)
        f.close()
        app_text += app_structure.format(app.title(),os.path.join("_source",app.replace(".","_")))
        #includes += include_text.format(app.replace(".","_"))

    text = file_content.format(app_text)
    f = open(os.path.join(src_path, "index.rst"),'w')
    f.write(text)
    f.close()











"""
.. automodule:: reference.models
   :members:
.. automodule:: reference.views
   :members:
.. automodule:: advanced
   :members:
.. automodule:: home
   :members:
.. automodule:: station
   :members:
.. automodule:: schedule
   :members:
.. automodule:: train.models
    :members:
.. automodule:: train.views
    :members:

"""
