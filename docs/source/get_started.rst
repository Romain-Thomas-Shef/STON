Getting started
===============

STON is composed of two different interfaces:

* The Command Line Interface [CLI]. It will help you start STON, run some tests, load/create configuration files.
* The Graphical User Interface [GUI]. This is the main part of STON and where you will browse/inspect/manipulate images. 

In this part of the documentation you will learn how to start STON and configure it. If you are interested about the GUI please have a look at the :doc:`main_window`.

Command line interface
----------------------

STON is started from a terminal (tested on Linux/MacOS/Windows) using the command line unterface. The command ``ston`` allows you to start the software with the default configuration (see next section). Other options are given in the command line interface. To have a look at them you can write ``ston --help``::


    usage: ston [-h] [--config CONFIG] [--makeconfig] [--test] [--version]

    ------------------------------------------------
     - STON: SofTware for petrOgraphic visualisatioN
     - Authors: R. Thomas & E. Dammer
     - Licence: GPLv3 -
    ------------------------------------------------

    options:
      -h, --help       show this help message and exit
      --config CONFIG  Configuration file. If no given,
                       STON will use default configuration
      --makeconfig     This command will create blank configuration file in the current directory
      --test           Run ston tests
      --version        show program's version number and exit
      


Four options (five if we count ``help``) are available to you:

* ``--config + Configfile``: This command allows you to start STON with your own configuration. You need to pass a configuration file to this argument (see next section).
* ``--makeconfig``: This will create a configuration file that you can modify in your current working directory.
* ``--test``: This will run the unittest of STON. See :doc:`tests` for more details.
* ``--version``: This just gives you the version of STON you are using.

Configuration file
------------------

STON is configured using configuration file. This allows you to tune STON to what you what you want it to look like and how you want it to work.

Format
^^^^^^

Configuration files are simple txt files. You can create one using the command ``ston --makeconfig``. This will give you a file called ``STON.conf`` in your current working directory. It looks like this::


    [Project_info]
    Name = to_be_changed
    Directory = to_be_changed
    Extensions = .tif;.png;.jpeg;.JPG;.JPEG;.jpg

    [General_image_display]
    Image_width = 200
    Downgrade_factor = 10

    [Meta_image_options]
    Downgrade_factor = 10
    Ncol_meta_image = 3
    Meta_txt_fontsize = 25
    name_on_images = Yes

    [Conf]
    main_window_width = 1150
    main_window_height = 700
    zoom_window_width = 900
    zoom_window_height = 400
    zoom_insert_pix_size = 50
    cluster_window_width = 900
    cluster_window_height = 400
    compare_window_width = 900
    compare_window_height = 400



It is composed of 4 sections which are all related to a different thing to configure:

* **Project_info**: This is where you can give a project name, the path to your images and what image extension STON must look for. So far STON has been tested with pngs, jpegs and tif files.

* **General_image_display**: On the :doc:`main_window` and :doc:`cluster_window`, images will appear as thumbnails on the window. You can adjust the quality and size of these thumbnails on this section of the configuration file. ``Image_width`` will let you adjust the size while ``downgrade factor`` allows you to lower slightly the quality. It is important to emphasize that for very heavy images, the downgrade factor is crucial to be able to manipulate the images smoothly.

* **Meta_image_options**: On the :doc:`cluster_window` window, you have the opportunity to create a *meta image*: an image that shows all the images in the cluster. This section helps you tune that image. ``Downgrade_factor`` helps you reduce the size of the individual images, ``ncol_meta_image`` will define how many columns the final image will contain. Finally, ``name_on_images`` and ``Meta_txt_fontsize`` allows you to define if you want the name of individual images on the meta image and what is the fontsize to be used.

* **Conf**: STON is composed of multiple windows that you can interact with. It might be annoying to resize windows each time you start the software to fit your screen. For that reason you can tune each window size in the configuration file. One important parameter is ``zoom_insert_pix_size``. If you go to :doc:`zoom_window` you will see at the bottom of the window, on the left, there is an small plot that allows you to see a more details section of the image. That parameter tune the size of that section (in pixel).


Default configuration
^^^^^^^^^^^^^^^^^^^^^

The default configuration is the same as the one given above. The only difference is that the directory (in section Project_info) is given as the output of following python command::


    from pathlib import Path
    directory = os.path.join(Path.home(), 'Documents')


.. warning::
    
    If you use the default configuration, all the images under ``Documents`` **AND** its subdirectories will be available from STON. This might look for a lot of images. We advise to use a personal configuration file to make sure that STON goes into the right directory.
