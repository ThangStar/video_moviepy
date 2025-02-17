# This Python file uses the following encoding: utf-8

from PySide6.QtCore import QThread, Signal
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, VideoClip, ColorClip
from proglog import ProgressBarLogger
from PIL import Image
import numpy as np
from moviepy.audio.AudioClip import concatenate_audioclips
# CONFIG VIDEO
TOTAL_WIDTH = 1920  
SCREEN_HEIGHT = 1080
IMAGE_WIDTH = int(TOTAL_WIDTH / 4) 
IMAGE_HEIGHT = SCREEN_HEIGHT / 2

class VideoWorker(QThread):
    progress = Signal(str)
    finished = Signal(bool, str)
    msg = Signal(str)

    def __init__(self, media_items, save_path, background_music=None, video_config=None):
        super().__init__()
        
        self.media_items = media_items
        self.save_path = save_path
        self.background_music = background_music
        print(video_config)
        self.video_config = video_config or {
            "fps": 30,
            "bitrate": "2000k",
            "crf": 23,
            "width": 1280,
            "height": 720,
            "threads": 16
        }
        self.TOTAL_WIDTH = self.video_config["width"]
        self.SCREEN_HEIGHT = self.video_config["height"]
        self.IMAGE_WIDTH = int(self.TOTAL_WIDTH / 4) 
        self.IMAGE_HEIGHT = self.SCREEN_HEIGHT / 2
        
    def transform_image(self):
        if len(self.media_items) % 2 != 0:
            self.media_items.append(self.media_items[-1])
        # Xử lý ảnh theo cặp (2 ảnh/cặp)
        for i in range(0, len(self.media_items), 2):
            if i >= 8:  # Bắt đầu từ ảnh thứ 9
                # Tính toán số ảnh còn lại và tạo một ảnh rộng hơn
                remaining_images = len(self.media_items) - 8
                print(remaining_images)
                wide_image = Image.new('RGBA', (int(self.IMAGE_WIDTH * (remaining_images / 2)), self.SCREEN_HEIGHT))
                
                # Xử lý tất cả các ảnh còn lại
                for j in range(i, len(self.media_items), 2):
                    current_position = (j - 8) // 2 * self.IMAGE_WIDTH  # Vị trí x cho mỗi cặp ảnh
                    
                    # Xử lý ảnh đầu tiên trong cặp
                    img1_path, _ = self.media_items[j]
                    img1 = Image.open(img1_path)
                    img1 = img1.resize((self.IMAGE_WIDTH, int(self.IMAGE_HEIGHT)), Image.Resampling.LANCZOS)
                    wide_image.paste(img1, (current_position, 0))
                    
                    # Xử lý ảnh thứ hai trong cặp (nếu có)
                    if j + 1 < len(self.media_items):
                        img2_path, _ = self.media_items[j+1]
                        img2 = Image.open(img2_path)
                        img2 = img2.resize((self.IMAGE_WIDTH, int(self.IMAGE_HEIGHT)), Image.Resampling.LANCZOS)
                        wide_image.paste(img2, (current_position, int(self.SCREEN_HEIGHT/2)))
                
                # Lưu ảnh rộng cuối cùng
                wide_image.save(f"temp/images/process/combined_4.png")
                break
            
            elif i + 1 < len(self.media_items):  # Xử lý các ảnh từ 0-8 như bình thường
                # Lấy 2 ảnh liên tiếp
                img1_path, _ = self.media_items[i]
                img2_path, _ = self.media_items[i+1]
                
                # Xử lý ảnh thứ nhất
                img1 = Image.open(img1_path)
                img1 = img1.resize((self.IMAGE_WIDTH, int(self.IMAGE_HEIGHT)), Image.Resampling.LANCZOS)
                
                # Xử lý ảnh thứ hai
                img2 = Image.open(img2_path)
                img2 = img2.resize((self.IMAGE_WIDTH, int(self.IMAGE_HEIGHT)), Image.Resampling.LANCZOS)
                
                # Tạo ảnh mới để ghép 2 ảnh theo chiều dọc
                combined_image = Image.new('RGBA', (self.IMAGE_WIDTH, self.SCREEN_HEIGHT))
                combined_image.paste(img1, (0, 0))
                combined_image.paste(img2, (0, int(self.SCREEN_HEIGHT/2)))
                
                # Lưu ảnh đã ghép
                combined_image.save(f"temp/images/process/combined_{i//2}.png")
            else:  # Xử lý ảnh cuối cùng nếu số ảnh là lẻ
                img_path, _ = self.media_items[i]
                img = Image.open(img_path)
                img = img.resize((self.IMAGE_WIDTH, int(self.IMAGE_HEIGHT)), Image.Resampling.LANCZOS)
                
                combined_image = Image.new('RGBA', (self.IMAGE_WIDTH, self.SCREEN_HEIGHT))
                combined_image.paste(img, (0, 0))
                
                combined_image.save(f"temp/images/process/combined_{i//2}.png")
        
        # Cập nhật lại danh sách media_items
        new_media_items = []
        for i in range(min(4, (len(self.media_items) + 1) // 2)):
            new_media_items.append((f'./temp/images/process/combined_{i}.png', f'combined_{i}'))
        
        if len(self.media_items) > 8:
            new_media_items.append((f'./temp/images/process/combined_4.png', f'combined_4'))
        
        self.media_items = new_media_items
    def run(self):
        self.transform_image()
        print("done")
        print(f"{self.media_items}")
        
        self.progress.emit("Đang tạo video từ ảnh...")
        
        image_duration = 3
        target_x = 10 - self.IMAGE_WIDTH  # Vị trí x mục tiêu để cạnh phải của hình = 10
        # Tính toán lại thời lượng video dựa trên thời điểm hình thứ 5 về vị trí target_x
        distance_to_move = (4 * self.IMAGE_WIDTH + self.IMAGE_WIDTH) - target_x  # Khoảng cách từ vị trí bắt đầu đến target_x
        movement_time = (distance_to_move / self.IMAGE_WIDTH) * image_duration
        
        # Tính toán thời gian dựa vào chiều dài ảnh cuối
        if len(self.media_items) > 4:
            last_image = ImageClip(self.media_items[-1][0])
            last_image_width = last_image.size[0]
            self.msg.emit(f"last_image_width: {last_image_width}")
            
            # Tính toán tổng khoảng cách cần di chuyển
            total_distance = last_image_width + self.TOTAL_WIDTH
            move_speed = 15  # pixels/giây
            
            # Tính thời gian di chuyển dựa trên tổng khoảng cách
            extra_duration_for_fifth_image = total_distance / move_speed
            
            # Đảm bảo thời gian tối thiểu là 5 giây
            extra_duration_for_fifth_image = max(extra_duration_for_fifth_image, 5)
        else:
            extra_duration_for_fifth_image = 0

        final_duration = 15 + extra_duration_for_fifth_image - 1
        self.msg.emit(f"final_duration: {final_duration}")
        
        def create_clip(img_path, index, start_time):
            # Tạo animation cho hình ảnh với nền trong suốt
            img = ImageClip(img_path)
            # Tính toán kích thước cho hình ảnh thứ 5
            if index < 4:
                img = img.resized(width=self.IMAGE_WIDTH, height=self.SCREEN_HEIGHT)
            else:
                # Giữ tỷ lệ khung hình nhưng đảm bảo chiều cao không vượt quá SCREEN_HEIGHT
                aspect_ratio = img.size[0] / img.size[1]
                new_height = self.SCREEN_HEIGHT
                new_width = int(new_height * aspect_ratio)
                img = img.resized(width=new_width, height=new_height)
            def make_frame(t):
                # Tính góc xoay (chỉ cho 4 ảnh đầu tiên)
                local_t = t - start_time
                if index < 4:  # Chỉ xoay 4 ảnh đầu
                    if local_t < 5:  # Giảm xuống 3 giây
                        progress = local_t / 5
                        # Thêm easing để xoay mượt mà hơn
                        eased_progress = 1 - (1 - progress) * (1 - progress)  # easeOutQuad
                        angle = 45 * (1 - eased_progress)
                    else:
                        angle = 0
                    
                    # Tạo clip mới với góc xoay tương ứng
                    rotated = VideoClip(lambda t: img.get_frame(0), duration=0.1)
                    if angle != 0:
                        import moviepy.video.fx as vfx
                        rotated = vfx.Rotate(angle=angle, unit='deg', expand=True, resample='bicubic', bg_color=None).apply(rotated)
                    return rotated.get_frame(0)
                else:
                    # Không xoay cho các ảnh từ index 4 trở đi
                    return img.get_frame(0)
            self.is_last_image = False
            
            def create_position(t):
                local_t = t - start_time
                if t < start_time:
                    return (self.TOTAL_WIDTH, 0)
                elif local_t < 5.1 and not self.is_last_image:
                    if index >= 4 and self.is_last_image == False:
                        self.is_last_image = True
                        return (4 * self.IMAGE_WIDTH + self.IMAGE_WIDTH, 0)
                    elif index < 4:
                        final_x = index * self.IMAGE_WIDTH
                        progress = local_t / 5
                        eased_progress = 1 - (1 - progress) * (1 - progress)
                        current_x = self.TOTAL_WIDTH - (self.TOTAL_WIDTH - final_x) * eased_progress
                        return (current_x, 0)
                else:
                    current_time = t
                    
                    # Đảm bảo vị trí x không vượt quá giới hạn màn hình
                    if index < 4:
                        initial_x = index * self.IMAGE_WIDTH
                    else:
                        initial_x = 4 * self.IMAGE_WIDTH + (index - 4) * self.IMAGE_WIDTH
                    
                    time_since_movement = current_time - (5 * image_duration)
                    if time_since_movement > 0:
                        move_speed = 15
                        move_distance = time_since_movement * move_speed
                        new_x = initial_x - move_distance
                        # Bỏ giới hạn vị trí tối thiểu để hình cuối có thể di chuyển hết màn hình
                        if index < 4:
                            new_x = max(new_x, -self.IMAGE_WIDTH)  # Giới hạn chỉ cho 4 hình đầu
                    else:
                        new_x = initial_x
                    
                    return (int(new_x), 0)
        
            # Tạo clip với hiệu ứng
            clip = VideoClip(make_frame, duration=final_duration)
            clip = clip.with_position(create_position)
            return clip
        
        # Tạo các clips
        clips = []
        for i, (img_path, _) in enumerate(self.media_items):
            clip = create_clip(img_path, i, i * image_duration)
            clips.append(clip)
        # Tạo video cuối cùng
        # final_bg = ColorClip(size=(self.TOTAL_WIDTH, self.SCREEN_HEIGHT), color=(0,0,0)).with_duration(final_duration)  # Đổi màu nền thành trắng và bỏ alpha
        final_clip = CompositeVideoClip(clips, size=(self.TOTAL_WIDTH, self.SCREEN_HEIGHT))  # Bỏ bg_color=None
        
        # Thêm nhạc nền nếu có
        if self.background_music:
            self.progress.emit("Đang thêm nhạc nền...")
            audio = AudioFileClip(self.background_music)
            
            # Tính toán số lần lặp cần thiết
            num_loops = int(np.ceil(final_clip.duration / audio.duration))
            # Tạo audio mới bằng cách nối nhiều bản sao
            concatenated_audio = concatenate_audioclips([audio] * num_loops)
            # Cắt đúng độ dài cần thiết
            final_audio = concatenated_audio.subclipped(0, final_clip.duration)
            
            final_clip = final_clip.with_audio(final_audio)
        
        class MyBarLogger(ProgressBarLogger):
            def __init__(self, worker):
                super().__init__()
                self.worker = worker

            def bars_callback(self, bar, attr, value, old_value=None):
                percentage = (value / self.bars[bar]['total']) * 100
                self.worker.progress.emit(f"Progress: {percentage:.1f}%")
        
        # Khởi tạo logger với tham chiếu đến worker
        logger = MyBarLogger(self)

        # Xuất video
        self.progress.emit("Đang xuất video...")
        final_clip.write_videofile(
            self.save_path,
            fps=self.video_config["fps"],
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=self.video_config["threads"],
            bitrate=self.video_config["bitrate"],
            ffmpeg_params=[
                "-pix_fmt", "yuv420p",
                "-crf", str(self.video_config["crf"]),
                "-tune", "film"
            ],
            logger=logger 
        )
        
        # Dọn dẹp
        final_clip.close()
        if self.background_music and "audio" in locals():
            audio.close()
        
        self.finished.emit(True, "Tạo video thành công!")
