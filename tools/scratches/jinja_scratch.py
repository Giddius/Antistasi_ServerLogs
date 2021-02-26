from jinja2 import Environment, FileSystemLoader, contextfunction, Undefined, meta
import jinja2
from pprint import pprint


missing_vars = []


class GidUndefined(jinja2.Undefined):

    def _add_missing_var(self):
        missing_vars.append(self._undefined_name)

    def __iter__(self):
        self._add_missing_var()
        return super().__iter__()

    def __str__(self):
        self._add_missing_var()
        return super().__str__()

    def __len__(self):
        self._add_missing_var()
        return super().__len__()

    def __eq__(self):
        self._add_missing_var()
        return super().__eq__()

    def __ne__(self):
        self._add_missing_var()
        return super().__eq__()

    def __bool__(self):
        self._add_missing_var()
        return super().__e__bool__q__()

    def __hash__(self):
        self._add_missing_var()
        return super().__hash__()


env = Environment(undefined=GidUndefined, loader=FileSystemLoader(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\docs\resources\templates"))

template_source = env.loader.get_source(env, "glossary_template.md.jinja")
parsed_content = env.parse(template_source)
x = meta.find_undeclared_variables(parsed_content)
pprint(x)
print('#' * 50)
pprint(missing_vars)
