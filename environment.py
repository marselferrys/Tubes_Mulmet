import time
import numpy as np

class Environment:
    """
    Kelas Environment mengelola aturan permainan, status lampu lalu lintas (hijau/merah), timer,
    serta kondisi menang/kalah dalam permainan. Digunakan untuk simulasi lingkungan permainan
    yang berubah-ubah secara acak sesuai parameter yang diberikan.
    """

    def __init__(self, window_width=800, green_duration_range=(2, 5), red_duration_range=(1, 3), game_duration_range=(50, 61)):
        """
        Inisialisasi environment dengan pengaturan awal.

        Parameters:
            window_width (int): Lebar jendela permainan untuk menentukan posisi garis finish.
            green_duration_range (tuple): Rentang durasi lampu hijau (min, max) dalam detik.
            red_duration_range (tuple): Rentang durasi lampu merah (min, max) dalam detik.
            game_duration_range (tuple): Rentang durasi total permainan (min, max) dalam detik.
        """

        # Garis finish horizontal sebagai target pemain
        self.finish_line_x = window_width - 160  # Sesuaikan dengan ukuran karakter/player

        # Status lampu lalu lintas: "initial", "green", atau "red"
        self.light_status = "initial"

        # Rentang durasi lampu hijau dan merah serta durasi total permainan
        self.green_duration_range = green_duration_range
        self.red_duration_range = red_duration_range
        self.game_duration_range = game_duration_range

        # Durasi dan waktu mulai untuk lampu hijau
        self.green_duration = 0
        self.green_start_time = 0

        # Durasi tetap dan waktu mulai untuk lampu merah
        self.red_duration = 0
        self.red_light_start_time = 0

        # Waktu mulai permainan dan durasi total permainan
        self.game_start_time = 0
        self.total_game_duration = 0

        # Waktu jeda total dan status pause
        self.paused_time_total = 0
        self.pause_start_time = None
        self.is_paused = False

        # Waktu jeda lampu hijau
        self.green_paused_time = 0
        self.green_pause_start = None

        # Waktu jeda lampu merah
        self.red_paused_time = 0
        self.red_pause_start = None


    def reset(self):
        """
        Mengatur ulang semua parameter lingkungan untuk memulai permainan baru.
        Digunakan saat restart permainan setelah menang/kalah.
        """
        self.light_status = "initial"
        self.green_duration = 0
        self.green_start_time = 0
        self.red_light_start_time = 0
        self.game_start_time = 0

        # Menetapkan durasi total permainan secara acak dari range
        self.total_game_duration = np.random.randint(*self.game_duration_range)

        self.is_paused = False
        self.pause_start_time = None
        self.paused_time_total = 0

        self.green_paused_time = 0
        self.green_pause_start = None

        self.red_paused_time = 0
        self.red_pause_start = None


    def start_game_timer(self):
        """
        Memulai timer utama permainan.
        Harus dipanggil sebelum permainan dimulai.
        """
        self.game_start_time = time.time()


    def switch_to_green_light(self):
        """
        Mengganti status lampu ke hijau dan menetapkan durasinya secara acak.
        Digunakan untuk beralih ke fase lampu hijau.
        """
        self.light_status = "green"
        self.green_start_time = time.time()
        self.green_duration = np.random.randint(*self.green_duration_range)
        self.green_paused_time = 0
        self.green_pause_start = None
        print(f"Green Light for {self.green_duration} seconds.")


    def switch_to_red_light(self):
        """
        Mengganti status lampu ke merah dan menetapkan durasinya secara acak.
        Digunakan untuk beralih ke fase lampu merah.
        """
        self.light_status = "red"
        self.red_light_start_time = time.time()
        self.red_duration = np.random.randint(*self.red_duration_range)
        self.red_paused_time = 0
        self.red_pause_start = None
        print(f"Red Light for {self.red_duration} seconds.")


    def is_green_light(self):
        """
        Memeriksa apakah lampu saat ini berwarna hijau.

        Returns:
            bool: True jika lampu hijau, False selain itu.
        """
        return self.light_status == "green"


    def is_red_light(self):
        """
        Memeriksa apakah lampu saat ini berwarna merah.

        Returns:
            bool: True jika lampu merah, False selain itu.
        """
        return self.light_status == "red"


    def is_initial_state(self):
        """
        Memeriksa apakah permainan masih dalam kondisi awal (menunggu).
        Tidak ada lampu menyala.

        Returns:
            bool: True jika status 'initial', False selainnya.
        """
        return self.light_status == "initial"


    def get_remaining_green_time(self):
        """
        Mendapatkan sisa waktu lampu hijau.

        Returns:
            float: Sisa waktu lampu hijau dalam detik.
        """
        if self.is_green_light():
            if self.is_paused:
                elapsed = self.green_pause_start - self.green_start_time - self.green_paused_time
            else:
                elapsed = time.time() - self.green_start_time - self.green_paused_time
            return max(0, self.green_duration - elapsed)
        return 0


    def get_remaining_red_time(self):
        """
        Mendapatkan sisa waktu lampu merah.

        Returns:
            float: Sisa waktu lampu merah dalam detik.
        """
        if self.is_red_light():
            if self.is_paused:
                elapsed = self.red_pause_start - self.red_light_start_time - self.red_paused_time
            else:
                elapsed = time.time() - self.red_light_start_time - self.red_paused_time
            return max(0, self.red_duration - elapsed)
        return 0


    def is_green_light_over(self):
        """
        Memeriksa apakah durasi lampu hijau telah habis.

        Returns:
            bool: True jika lampu hijau sudah selesai, False selainnya.
        """
        return self.is_green_light() and (time.time() - self.green_start_time) >= self.green_duration


    def is_red_light_over(self):
        """
        Memeriksa apakah durasi lampu merah telah habis.

        Returns:
            bool: True jika lampu merah sudah selesai, False selainnya.
        """
        return self.is_red_light() and (time.time() - self.red_light_start_time) >= self.red_duration


    def get_remaining_game_time(self):
        """
        Mendapatkan sisa waktu permainan keseluruhan.

        Returns:
            float: Sisa waktu permainan dalam detik.
        """
        if self.game_start_time == 0:
            return self.total_game_duration
        if self.is_paused:
            elapsed = self.pause_start_time - self.game_start_time - self.paused_time_total
        else:
            elapsed = time.time() - self.game_start_time - self.paused_time_total
        return max(0, self.total_game_duration - elapsed)


    def has_game_time_elapsed(self):
        """
        Memeriksa apakah waktu total permainan telah habis.

        Returns:
            bool: True jika waktu permainan habis, False selainnya.
        """
        if self.game_start_time == 0:
            return False  # Permainan belum dimulai
        return (time.time() - self.game_start_time) >= self.total_game_duration


    def reached_finish_line(self, player_x):
        """
        Memeriksa apakah pemain telah mencapai garis finish.

        Parameters:
            player_x (float): Posisi horizontal pemain (koordinat x).

        Returns:
            bool: True jika pemain melewati garis finish, False selainnya.
        """
        return player_x > self.finish_line_x + 20


    def pause(self):
        """
        Menjeda permainan dan mencatat waktu jeda.
        """
        if not self.is_paused:
            self.is_paused = True
            self.pause_start_time = time.time()

            if self.is_green_light():
                self.green_pause_start = time.time()
            elif self.is_red_light():
                self.red_pause_start = time.time()


    def resume(self):
        """
        Melanjutkan permainan yang sempat dijeda.
        """
        if self.is_paused:
            pause_duration = time.time() - self.pause_start_time
            self.paused_time_total += pause_duration

            if self.is_green_light() and self.green_pause_start is not None:
                self.green_paused_time += time.time() - self.green_pause_start

            if self.is_red_light() and self.red_pause_start is not None:
                self.red_paused_time += time.time() - self.red_pause_start

            self.is_paused = False
            self.pause_start_time = None
            self.green_pause_start = None
            self.red_pause_start = None