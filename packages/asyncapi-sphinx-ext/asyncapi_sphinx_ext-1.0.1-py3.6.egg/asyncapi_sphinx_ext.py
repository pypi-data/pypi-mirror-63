
from ruamel.yaml import YAML
from collections import defaultdict

from typing import Any, Dict, IO, List, Pattern, Set, Tuple, Iterable
from typing import cast

from sphinx import addnodes
from sphinx import roles
from sphinx.locale import _, __
from sphinx.domains import Domain
from sphinx.environment import BuildEnvironment
from sphinx.util.docutils import SphinxDirective, new_document
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.inspect import safe_getattr

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives.admonitions import BaseAdmonition

class asyncapi_node(nodes.Admonition, nodes.Element):
    pass

class asyncapi_overview(nodes.General,nodes.Element):
    pass

def visit_asyncapi_html(self, node):
    self.body.append(self.starttag(node, 'asyncapi_overview'))

def depart_asyncapi_html(self, node):
    self.body.append('</asyncapi_overview>')

def visit_asyncapi_node(self, node):
    self.visit_admonition(node)

def depart_asyncapi_node(self, node):
    self.depart_admonition(node)

class AsyncApiChannelDirective(BaseAdmonition,SphinxDirective):
    node_class = asyncapi_node
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'class': directives.class_option,
        'name': directives.unchanged,
    }
    yaml = YAML()

    def run(self):
        # use all the text
        as_admonition = len(self.arguments) and self.arguments[0] == 'admonition'
        if as_admonition:
            (channel,) = super().run()  # type: Tuple[Node]
        else:
            channel = self.node_class('')
        # parse asyncapi spec
        channel['asyncapi'] = res = self.yaml.load('\n'.join(self.content))
        channel['docname'] = self.env.docname
        self.add_name(channel)
        self.set_source_info(channel)
        self.state.document.note_explicit_target(channel)
        if not as_admonition:
            for topic,topic_spec in res.items():
                for operation,operation_spec in topic_spec.items():
                    if operation == 'publish':
                        op = 'PUB'
                    elif operation == 'subscribe':
                        op = 'SUB'
                    message_spec = operation_spec.get('message',{})
                    p = nodes.strong(text=topic)
                    # channel.append(nodes.strong(text=op))
                    channel.append(p)
                    p = nodes.paragraph()
                    p.append(nodes.inline(text=op,classes=['guilabel']))
                    if 'contentType' in message_spec:
                        p.append(nodes.inline(text=' '))
                        p.append(nodes.inline(text=message_spec['contentType'],classes=['guilabel']))
                    channel.append(p)
                    p = nodes.paragraph()
                    p.append(nodes.emphasis(text=operation_spec.get('summary','')))
                    channel.append(p)
                    for key,spec in message_spec.get('payload',{}).get('properties',{}).items():
                        fl = nodes.field_list()
                        field = nodes.field()
                        field.append(nodes.field_name(key,nodes.Text(key)))
                        field.append(nodes.field_body('spec',self.make_property_spec(spec)))
                        fl.append(field)
                        channel.append(fl)
                    channel.append(nodes.paragraph())
        return [channel]

    def make_property_spec(self,property_spec):
        fl = nodes.field_list()
        for key,value in property_spec.items():
            field = nodes.field()
            field.append(nodes.field_name(key,nodes.Text(key)))
            field.append(nodes.field_body(value,nodes.Text(value)))
            fl.append(field)
        return fl

class AsynApiDomain(Domain):
    name = 'asyncapi'
    label = 'asyncapi'

    @property
    def channels(self) -> Dict[str, List[asyncapi_node]]:
        return self.data.setdefault('channels', {})

    def clear_doc(self, docname: str) -> None:
        self.channels.pop(docname, None)

    def merge_domaindata(self, docnames: List[str], otherdata: Dict) -> None:
        for docname in docnames:
            self.channels[docname] = otherdata['asyncapi'][docname]

    def process_doc(self, env: BuildEnvironment, docname: str,
                    document: nodes.document) -> None:
        channels = self.channels.setdefault(docname, [])
        for channel in document.traverse(asyncapi_node):
            env.app.emit('asyncapi_channel-defined', channel)
            channels.append(channel)

class AsyncApiDirective(SphinxDirective):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'class': directives.class_option,
        'name': directives.unchanged,
    }

    def run(self):
        # Simply insert an empty node which will be replaced later
        return [asyncapi_overview('',operation=self.arguments[0])]

class AsyncApiChannelProcessor:
    def __init__(self, app, doctree, docname):
        self.builder = app.builder
        self.config = app.config
        self.env = app.env
        self.domain = app.env.get_domain('asyncapi')

        self.process(doctree, docname)


    def create_table(self):
        table = nodes.table()
        tgroup = nodes.tgroup(cols=2)
        table += tgroup
        for colwidth in (30,70):
            tgroup += nodes.colspec(colwidth=colwidth)

        thead = nodes.thead()
        tgroup += thead
        # thead += self.create_table_row(('Topic','summary'))

        tbody = nodes.tbody()
        tgroup += tbody
        return table,tbody


    def process(self, doctree: nodes.document, docname: str) -> None:
        channels = sum(self.domain.channels.values(), [])  # type: List[todo_node]
        document = new_document('')

        for node in doctree.traverse(asyncapi_overview):
            wanted_operation = node['operation']

            if node.get('ids'):
                content = [nodes.target()]  # type: List[Element]
            else:
                content = []
            table,tbody = self.create_table()
            per_topic = defaultdict(list)
            for channel in channels:
                for topic,topic_spec in channel['asyncapi'].items():
                    for operation,op_spec in topic_spec.items():
                        if operation == wanted_operation:
                            source = channel.source.split(' of ')[1]
                            ref = self.create_channel_reference(source,channel, docname)
                            per_topic[topic].append((op_spec['summary'],ref))
            for topic,topic_spec in per_topic.items():
                summary = topic_spec[0][0]
                desc_node = nodes.inline(text=summary)
                for _,link in topic_spec:
                    desc_node.append(nodes.inline(text=', '))
                    desc_node.append(link)
                tbody.append(
                    self.create_table_row(
                        (topic,desc_node)
                    )
                )
            node.replace_self(table)

    def create_table_row(self, row_cells):
        row = nodes.row()
        for cell in row_cells:
            entry = nodes.entry()
            row.append(entry)
            if isinstance(cell,str):
                entry.append(nodes.paragraph(text=cell))
            else:
                entry.append(cell)
        return row


    def create_channel_reference(self, text:str,channel: asyncapi_node, docname: str) -> nodes.paragraph:
        para = nodes.inline(classes=['asyncapi-source'])

        # Create a reference
        linktext = nodes.emphasis(text,text)
        reference = nodes.reference('', '', linktext, internal=True)
        try:
            reference['refuri'] = self.builder.get_relative_uri(docname, channel['docname'])
            reference['refuri'] += '#' + channel['ids'][0]
        except NoUri:
            # ignore if no URI can be determined, e.g. for LaTeX output
            pass

        para += reference

        return para

class AsyncApiBuilder(Builder):
    """
    Evaluates coverage of code in the documentation.
    """
    name = 'asyncapi'
    epilog = __('Testing of coverage in the sources finished, look at the '
                'results in %(outdir)s' + path.sep + 'python.txt.')

    def get_outdated_docs(self) -> str:
        return 'coverage overview'

    def write(self, *ignored: Any) -> None:
        print(self.env.domaindata)

    def __old(self):
        self.py_undoc = {}  # type: Dict[str, Dict[str, Any]]
        self.build_py_coverage()
        self.write_py_coverage()

        self.c_undoc = {}  # type: Dict[str, Set[Tuple[str, str]]]
        self.build_c_coverage()
        self.write_c_coverage()

    def build_c_coverage(self) -> None:
        # Fetch all the info from the header files
        c_objects = self.env.domaindata['c']['objects']
        for filename in self.c_sourcefiles:
            undoc = set()  # type: Set[Tuple[str, str]]
            with open(filename) as f:
                for line in f:
                    for key, regex in self.c_regexes:
                        match = regex.match(line)
                        if match:
                            name = match.groups()[0]
                            if name not in c_objects:
                                for exp in self.c_ignorexps.get(key, []):
                                    if exp.match(name):
                                        break
                                else:
                                    undoc.add((key, name))
                            continue
            if undoc:
                self.c_undoc[filename] = undoc

    def write_c_coverage(self) -> None:
        output_file = path.join(self.outdir, 'c.txt')
        with open(output_file, 'w') as op:
            if self.config.coverage_write_headline:
                write_header(op, 'Undocumented C API elements', '=')
            op.write('\n')

            for filename, undoc in self.c_undoc.items():
                write_header(op, filename)
                for typ, name in sorted(undoc):
                    op.write(' * %-50s [%9s]\n' % (name, typ))
                op.write('\n')

    def ignore_pyobj(self, full_name: str) -> bool:
        for exp in self.py_ignorexps:
            if exp.search(full_name):
                return True
        return False

    def build_py_coverage(self) -> None:
        objects = self.env.domaindata['py']['objects']
        modules = self.env.domaindata['py']['modules']

        skip_undoc = self.config.coverage_skip_undoc_in_source

        for mod_name in modules:
            ignore = False
            for exp in self.mod_ignorexps:
                if exp.match(mod_name):
                    ignore = True
                    break
            if ignore or self.ignore_pyobj(mod_name):
                continue

            try:
                mod = import_module(mod_name)
            except ImportError as err:
                logger.warning(__('module %s could not be imported: %s'), mod_name, err)
                self.py_undoc[mod_name] = {'error': err}
                continue

            funcs = []
            classes = {}  # type: Dict[str, List[str]]

            for name, obj in inspect.getmembers(mod):
                # diverse module attributes are ignored:
                if name[0] == '_':
                    # begins in an underscore
                    continue
                if not hasattr(obj, '__module__'):
                    # cannot be attributed to a module
                    continue
                if obj.__module__ != mod_name:
                    # is not defined in this module
                    continue

                full_name = '%s.%s' % (mod_name, name)
                if self.ignore_pyobj(full_name):
                    continue

                if inspect.isfunction(obj):
                    if full_name not in objects:
                        for exp in self.fun_ignorexps:
                            if exp.match(name):
                                break
                        else:
                            if skip_undoc and not obj.__doc__:
                                continue
                            funcs.append(name)
                elif inspect.isclass(obj):
                    for exp in self.cls_ignorexps:
                        if exp.match(name):
                            break
                    else:
                        if full_name not in objects:
                            if skip_undoc and not obj.__doc__:
                                continue
                            # not documented at all
                            classes[name] = []
                            continue

                        attrs = []  # type: List[str]

                        for attr_name in dir(obj):
                            if attr_name not in obj.__dict__:
                                continue
                            try:
                                attr = safe_getattr(obj, attr_name)
                            except AttributeError:
                                continue
                            if not (inspect.ismethod(attr) or
                                    inspect.isfunction(attr)):
                                continue
                            if attr_name[0] == '_':
                                # starts with an underscore, ignore it
                                continue
                            if skip_undoc and not attr.__doc__:
                                # skip methods without docstring if wished
                                continue
                            full_attr_name = '%s.%s' % (full_name, attr_name)
                            if self.ignore_pyobj(full_attr_name):
                                continue
                            if full_attr_name not in objects:
                                attrs.append(attr_name)
                        if attrs:
                            # some attributes are undocumented
                            classes[name] = attrs

            self.py_undoc[mod_name] = {'funcs': funcs, 'classes': classes}

    def write_py_coverage(self) -> None:
        output_file = path.join(self.outdir, 'python.txt')
        failed = []
        with open(output_file, 'w') as op:
            if self.config.coverage_write_headline:
                write_header(op, 'Undocumented Python objects', '=')
            keys = sorted(self.py_undoc.keys())
            for name in keys:
                undoc = self.py_undoc[name]
                if 'error' in undoc:
                    failed.append((name, undoc['error']))
                else:
                    if not undoc['classes'] and not undoc['funcs']:
                        continue

                    write_header(op, name)
                    if undoc['funcs']:
                        op.write('Functions:\n')
                        op.writelines(' * %s\n' % x for x in undoc['funcs'])
                        op.write('\n')
                    if undoc['classes']:
                        op.write('Classes:\n')
                        for name, methods in sorted(
                                undoc['classes'].items()):
                            if not methods:
                                op.write(' * %s\n' % name)
                            else:
                                op.write(' * %s -- missing methods:\n\n' % name)
                                op.writelines('   - %s\n' % x for x in methods)
                        op.write('\n')

            if failed:
                write_header(op, 'Modules that failed to import')
                op.writelines(' * %s -- %s\n' % x for x in failed)

    def finish(self) -> None:
        # dump the coverage data to a pickle file too
        picklepath = path.join(self.outdir, 'undoc.pickle')
        with open(picklepath, 'wb') as dumpfile:
            pickle.dump((self.py_undoc, self.c_undoc), dumpfile)

def setup(app):
    data = []
    app.setup_extension('sphinx.ext.autodoc')
    app.add_config_value('asyncapi_link_only', True, 'html')
    app.add_node(asyncapi_node,html=(visit_asyncapi_node,depart_asyncapi_node))
    app.add_node(asyncapi_overview)
    app.add_directive('asyncapi_channels', AsyncApiChannelDirective)
    app.add_directive('asyncapi_overview', AsyncApiDirective)
    app.add_domain(AsynApiDomain)
    app.connect('doctree-resolved', AsyncApiChannelProcessor)
    app.add_builder(AsyncApiBuilder)
