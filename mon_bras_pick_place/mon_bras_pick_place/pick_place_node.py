#!/usr/bin/env python3
"""
Pick and Place simulation using MuJoCo Python bindings.
Robot arm: uFactory Lite6 (6-DOF)
"""

import mujoco # pyright: ignore[reportMissingImports]
import mujoco.viewer # type: ignore
import numpy as np # pyright: ignore[reportMissingImports]
import time
import threading
import os
import sys

def find_xml_file():
    """Find the scene XML file."""
    possible_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'worlds', 'lite6_scene.xml'),
        os.path.join(os.path.dirname(__file__), '..', '..', 'worlds', 'lite6_scene.xml'),
        os.path.expanduser('~/ros2_ws/src/mon_bras_pick_place/worlds/lite6_scene.xml'),
    ]
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            return abs_path
    raise FileNotFoundError(f"Cannot find scene XML. Tried: {possible_paths}")

class PickAndPlaceSimulation:
    def __init__(self):
        xml_path = find_xml_file()
        print(f"Loading model from: {xml_path}")
        
        self.model = mujoco.MjModel.from_xml_path(xml_path)
        self.data = mujoco.MjData(self.model)
        
        print(f"\nModel loaded successfully!")
        print(f"Joints: {self.model.njnt}, Actuators: {self.model.nu}")
        
        self.running = True
        self.simulation_started = False
        
    def simulation_loop(self):
        """Main simulation loop."""
        print("\nStarting viewer... Close window to exit.\n")
        
        with mujoco.viewer.launch_passive(self.model, self.data) as viewer:
            self.simulation_started = True
            viewer.cam.distance = 2.5
            viewer.cam.azimuth = 160
            viewer.cam.elevation = -25
            
            while self.running and viewer.is_running():
                step_start = time.time()
                mujoco.mj_step(self.model, self.data)
                viewer.sync()
                time_until_next = self.model.opt.timestep - (time.time() - step_start)
                if time_until_next > 0:
                    time.sleep(time_until_next)
    
    def move_to_position(self, positions, duration=2.0):
        """Smooth movement to target positions."""
        positions = positions[:self.model.nu]
        print(f"  Moving: {[f'{p:.2f}' for p in positions]}")
        
        start_time = time.time()
        start_pos = self.data.ctrl[:len(positions)].copy()
        
        while time.time() - start_time < duration and self.running:
            elapsed = time.time() - start_time
            progress = min(elapsed / duration, 1.0)
            eased = progress * progress * (3 - 2 * progress)
            
            for i in range(len(positions)):
                self.data.ctrl[i] = start_pos[i] + (positions[i] - start_pos[i]) * eased
            time.sleep(0.01)
        
        for i in range(len(positions)):
            self.data.ctrl[i] = positions[i]
        time.sleep(0.3)
    
    def run_pick_place_sequence(self):
        """Execute pick-and-place."""
        while not self.simulation_started:
            time.sleep(0.1)
        time.sleep(1.5)
        
        print("\n" + "="*50)
        print("STARTING PICK AND PLACE")
        print("="*50 + "\n")
        
        sequences = [
            ([0.0, -0.5, 0.8, 0.0, 1.2, 0.0], 2.0, "1. Move above box"),
            ([0.0, -0.8, 1.0, 0.0, 1.2, 0.0], 2.0, "2. Lower to grasp"),
            ([0.0, -0.8, 1.0, 0.0, 0.3, 0.0], 1.0, "3. Close gripper"),
            ([0.0, -0.5, 0.8, 0.0, 0.3, 0.0], 2.0, "4. Lift box"),
            ([1.0, -0.5, 0.8, 0.0, 0.3, 0.0], 3.0, "5. Move to drop zone"),
            ([1.0, -0.8, 1.0, 0.0, 0.3, 0.0], 2.0, "6. Lower to place"),
            ([1.0, -0.8, 1.0, 0.0, 1.2, 0.0], 1.0, "7. Open gripper"),
            ([1.0, -0.5, 0.8, 0.0, 1.2, 0.0], 2.0, "8. Lift arm"),
            ([0.0, -0.5, 0.8, 0.0, 1.2, 0.0], 2.0, "9. Return home"),
        ]
        
        for pos, dur, desc in sequences:
            if not self.running:
                break
            print(f"\n>>> {desc}")
            self.move_to_position(pos, dur)
        
        print("\n" + "="*50)
        print(" SEQUENCE COMPLETE!")
        print("="*50 + "\n")
    
    def start(self):
        """Start everything."""
        sim_thread = threading.Thread(target=self.simulation_loop)
        sim_thread.daemon = True
        sim_thread.start()
        
        self.run_pick_place_sequence()
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False
        
        sim_thread.join(timeout=2.0)
        print("Done!")

def main():
    print("\n" + "="*60)
    print("  MUJOCO PICK AND PLACE - uFactory Lite6")
    print("="*60 + "\n")
    
    try:
        sim = PickAndPlaceSimulation()
        sim.start()
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()