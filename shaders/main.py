import moderngl_window as mglw

class App(mglw.WindowConfig):
    window_size = (1280, 720)
    resource_dir = 'programs'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.quad = mglw.geometry.quad_fs()
        self.prog = self.load_program(
            vertex_shader='vertex_shader.glsl',
            fragment_shader='fragment_shader.glsl'
        )
        self.set_uniform('iResolution', self.window_size)
        # Add these lines to your __init__ method to set the uniform values
        self.prog['iTime'] = 0.0  # You can update this with the actual time
        self.prog['iResolution'] = self.window_size  # You can update this with the actual screen resolution

    
    
        
    def set_uniform(self, u_name, u_value):
        try:
            self.prog[u_name].value = u_value
        except KeyError:
            print(f'Uniform {u_name} not found in shader')
    
    def render(self, time, frametime):
        self.ctx.clear()
        self.prog['iTime'] = time  # Update 'iTime' with the current time
        self.quad.render(self.prog)
        
        
if __name__ == '__main__':
    mglw.run_window_config(App)