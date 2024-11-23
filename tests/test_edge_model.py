import unittest
from src.modeling.edge_model import (
    unidirectional_wave,
    merged_wave,
    edge_intensity,
    merged_intensity,
)

class TestEdgeModel(unittest.TestCase):
    def test_unidirectional_wave(self):
        print("\n--- Test: unidirectional_wave ---")
        time, wave = unidirectional_wave(5, 2, 10)
        print(f"Generated time array (first 5 points): {time[:5]}")
        print(f"Generated wave array (first 5 points): {wave[:5]}")
        self.assertEqual(len(time), 100, "Time array should have 100 points")
    
    def test_unidirectional_wave(self):
        print("\n--- Test: unidirectional_wave ---")
        time, wave = unidirectional_wave(5, 2, 10)
        print(f"Generated time array (first 5 points): {time[:5]}")
        print(f"Generated wave array (first 5 points): {wave[:5]}")
        self.assertEqual(len(time), 100, "Time array should have 100 points")
        self.assertAlmostEqual(max(wave), 2, delta=0.1, msg="Max amplitude should be close to 2")


    def test_edge_intensity(self):
        print("\n--- Test: edge_intensity ---")
        frequency = 5
        amplitude = 2
        intensity = edge_intensity(frequency, amplitude)
        print(f"Edge intensity calculated: {intensity}")
        self.assertEqual(intensity, 10, "Edge intensity should equal frequency * amplitude")

    def test_merged_wave(self):
        print("\n--- Test: merged_wave ---")
        wave_A = [1, 2, 3]
        wave_B = [3, 2, 1]
        merged = merged_wave(wave_A, wave_B)
        print(f"Merged wave: {merged}")
        self.assertEqual(merged, [4, 4, 4], "Merged wave should be the sum of both waves")

    def test_merged_intensity(self):
        print("\n--- Test: merged_intensity ---")
        freq_a_b, amp_a_b = 5, 2
        freq_b_a, amp_b_a = 3, 4
        intensity = merged_intensity(freq_a_b, amp_a_b, freq_b_a, amp_b_a)
        print(f"Frequencies: A->B={freq_a_b}, B->A={freq_b_a}")
        print(f"Amplitudes: A->B={amp_a_b}, B->A={amp_b_a}")
        print(f"Merged intensity calculated: {intensity}")
        expected_intensity = (freq_a_b * amp_a_b) + (freq_b_a * amp_b_a)
        self.assertEqual(intensity, expected_intensity, "Merged intensity should be the sum of both directions")

    def test_zero_frequency_or_amplitude(self):
        print("\n--- Test: Zero frequency or amplitude ---")
        
        # Test zero frequency
        time, wave = unidirectional_wave(0, 2, 10)
        print(f"Wave with zero frequency (first 5 points): {wave[:5]}")
        self.assertTrue(all(val == 0 for val in wave), "Wave should be all zeros when frequency is 0")
        
        # Test zero amplitude
        time, wave = unidirectional_wave(5, 0, 10)
        print(f"Wave with zero amplitude (first 5 points): {wave[:5]}")
        self.assertTrue(all(val == 0 for val in wave), "Wave should be all zeros when amplitude is 0")

if __name__ == "__main__":
    unittest.main()

