====
fitb
====

A practical program extension system.

``fitb`` lets you define *extension points* which are named points in your program that can be extended externally. Each
extension point can any number of *extensions* associated with it, each providing a different method of extension at
that point. Each extension can be configured with *configuration options* that it defines.

Given an extension point with a number of extensions each accepting their own set of configuration options, ``fitb``
makes it easy to construct a default configuration. You can take this default configuration, modify as you see fit (e.g.
by loading configuration data from a file), and then *activate* the extension with the configuration. Activation tells
each extension to actually instantiate some object which fulfills the role of extending the extension point.

A motivating example
====================

Suppose you had a program that performed some complex calculation and then reported the result to a user. The nature
of the reporting could be to file, to screen, to a database, or in ways you can't think of right now. To account for
this reporting flexibility, you'd like your program reporting to be *extensible*; users should be able to provide new
kinds of reporting **without you needing to change your program**. This is where ``fitb`` comes in.

With ``fitb``, you'd define an extension point for reporting. Extension points are named, so let's cleverly call the
point "reporting". Then you'd add extensions to the extension point for each of the kinds of reports you want to
generate. Critically, other developers can add extensions as well without you having to modify your program.

Each extension will have a name, so let's consider one called "pdf" that produces a PDF. A critical part of the PDF is
the font name and size it will use, so the PDF extension will define two configurable options, "font-size" and
"font-name", each with a default value. Other extensions will have options for their own specific needs.

With the extension point and extensions in place, you can then create a configuration - really just a specially
structured dictionary - describing the default config that you can modify if you want. Then, you can activate the
extension point with the configuration, thereby asking each reporting extension to instantiate a reporting object based
on the information in the configuration. With your collection of reporting extensions available, the user can select
which they want to use by specifying the name of the extension they want.

What are configurations?
========================

.. TODO: Describe the idea of configurations, extension-point sub-config, extension-subconfigs, and so forth.

Concrete examples
=================

See the "examples" directory for examples of how to use fitb.
