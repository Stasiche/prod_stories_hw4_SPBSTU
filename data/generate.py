import bpy
import random
import uuid
import math
import datetime
import os
from argparse import ArgumentParser
import sys

primitive_constructors = [
    bpy.ops.mesh.primitive_cube_add,
    bpy.ops.mesh.primitive_uv_sphere_add,
    bpy.ops.mesh.primitive_cylinder_add,
    bpy.ops.mesh.primitive_cone_add,
    bpy.ops.mesh.primitive_torus_add,
]
dpi = 2 * math.pi


def main(model_folder: str, k: int):
    if not os.path.exists(model_folder):
        os.mkdir(model_folder)

    with open(f"{model_folder}/labels.txt", 'w') as f:
        for ctor in random.choices(primitive_constructors, k=k):
            ctor()
            bpy.context.active_object.select_set(True)
            transform_seed = datetime.datetime.now().microsecond % 100
            print(transform_seed)
            bpy.ops.object.randomize_transform(
                random_seed=transform_seed,
                loc=(10, 10, 10),
                rot=(dpi, dpi, dpi),
                scale=(10, 10, 10),
            )
            fn = f"{uuid.uuid4()}.stl"
            bpy.ops.export_mesh.stl(
                filepath=os.path.join(model_folder, fn),
            )
            f.write(f'{fn}, {bpy.context.active_object.name}\n')
            bpy.ops.object.delete()


if __name__ == "__main__":
    # __arg_parser = ArgumentParser()
    # __arg_parser.add_argument('--models', type=str, help='Path to directory to save stl models')
    # __arg_parser.add_argument('-mn', type=int, default=100, help='Number of models to generate')
    #
    # __args = __arg_parser.parse_args()
    # main(__args.models, __args.k)

    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    print(argv)
    if len(argv) == 2:
        main(argv[0], int(argv[1]))
    else:
        main(argv[0], 100)
