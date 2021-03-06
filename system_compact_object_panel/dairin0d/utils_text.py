#  ***** BEGIN GPL LICENSE BLOCK *****
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  ***** END GPL LICENSE BLOCK *****

# <pep8 compliant>

import re

# Already implemented:
# bpy_extras.io_utils.unique_name(key, name, name_dict, name_max=-1, clean_func=None, sep='.')
#def unique_name(src_name, existing_names):
#    name = src_name
#    i = 1
#    while name in existing_names:
#        name = "{}.{:0>3}".format(src_name, i)
#        i += 1
#    return name

def compress_whitespace(s):
    return " ".join(s.split())
    #return re.sub("\\s+", " ", s).strip()

def indent(s, t):
    res = []
    for l in s.splitlines():
        res.append(t + l)
    return "\n".join(res)

def unindent(s, t):
    res = []
    nt = len(t)
    for l in s.splitlines():
        n1 = len(l)
        n0 = len(l.lstrip())
        nd = n1 - n0
        res.append(l[min(nt, nd):])
    return "\n".join(res)

def split_expressions(s, sep="\t", strip=False):
    if sep == "\t":
        text = s
    else:
        sep = sep.strip()
        text = ""
        brackets = 0
        for c in s:
            if c in "[{(":
                brackets += 1
            elif c in "]})":
                brackets -= 1
            if (brackets == 0) and (c == sep):
                c = "\t"
            text += c
    
    res = text.split("\t")
    return ([s.strip() for s in res] if strip else res)

def math_eval(s):
    try:
        return float(eval(s, math.__dict__))
    except Exception:
        # What actual exceptions can be raised by float/math/eval?
        return None

def vector_to_text(v, sep="\t", axes_names="xyzw"):
    sa = []
    for i in range(len(v)):
        s = str(v[i])
        if axes_names:
            s = axes_names[i] + ": " + s
        sa.append(s)
    return sep.join(sa)

def vector_from_text(v, s, sep="\t", axes_names="xyzw"):
    sa = split_expressions(s, sep, True)
    
    if axes_names:
        # first, check if there are keyword arguments
        kw = False
        
        for a in sa:
            if len(a) < 3:
                continue
            
            try:
                # list has no find() method
                i = axes_names.index(a[0].lower())
            except ValueError:
                i = -1
            
            if (i != -1) and (a[1] == ":"):
                v_i = math_eval(a[2:])
                if v_i is not None:
                    v[i] = v_i
                kw = True
        
        if kw:
            return
    
    for i in range(min(len(v), len(sa))):
        v_i = math_eval(sa[i])
        if v_i is not None:
            v[i] = v_i
