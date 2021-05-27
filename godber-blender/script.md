# DesertPy Blender Talk

## Demo 1 - Suzanne

### Draw 1 Suzanne

```python
import bpy

bpy.ops.mesh.primitive_monkey_add(location=(1,2,3))
```

### Draw 500 Suzannes

Clear with `a` then `x`.

```python
import bpy
from random import randint

number = 500

for i in range(0, number):
    x = randint(-10, 10)
    y = randint(-10, 10)
    z = randint(-4, 4)
    bpy.ops.mesh.primitive_monkey_add(location=(x,y,z))
```

### Clear All

This shows how to select all items and then delete them:

```python
import bpy
from random import randint

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

number = 500

for i in range(0, number):
    x = randint(-10, 10)
    y = randint(-10, 10)
    z = randint(-4, 4)
    bpy.ops.mesh.primitive_monkey_add(location=(x,y,z))
```

### Final

This last step demonstrates how to use the Info box to get function names:

* Right Click on a Suzanne head, choose Shade Smooth
* Look at output in Info Box, See `bpy.ops.object.shade_smooth()`
  
```python
import bpy
from random import randint

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

number = 500

for i in range(0, number):
    x = randint(-10, 10)
    y = randint(-10, 10)
    z = randint(-4, 4)
    bpy.ops.mesh.primitive_monkey_add(location=(x,y,z))
    bpy.ops.object.shade_smooth()
```

## Demo 2 - UI Thing

Next Time!
