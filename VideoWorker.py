
# This Python file uses the following encoding: utf-8

from PySide6.QtCore import QThread, Signal
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, VideoClip, ColorClip

class VideoWorker(QThread):
    progress = Signal(str)
    finished = Signal(bool, str)

    def __init__(self, media_items, save_path, background_music):
        super().__init__()
        self.media_items = media_items
        self.save_path = save_path
        self.background_music = background_music

    def run(self):
        self.progress.emit("Đang tạo video từ ảnh...")
        
        # Kích thước tổng thể của video
        total_width = 200  # Tổng chiều rộng video
        screen_height = 100
        image_duration = 5  # Thời gian mỗi hình
        image_width = 50  # Kích thước cố định cho mỗi hình    
        final_duration = len(self.media_items) * image_duration
        
        def ease_out(t):
            
            # Hàm Ease Out Cubic
            t = t / 5  # Chuẩn hóa thời gian về khoảng [0,1]
            return 1 - pow(1 - t, 3)
        
        def create_clip(img_path, index, start_time):
            # Tạo animation cho hình ảnh với nền trong suốt
            img = ImageClip(img_path, transparent=True)
            img = img.resized(width=image_width, height=screen_height)
            
            def make_frame(t):
                # Tính góc xoay
                local_t = t - start_time
                if local_t < 5:  # Kéo dài hiệu ứng xoay trong 5 giây
                    progress = ease_out(local_t)
                    angle = 45 * (1 - progress)  # Sử dụng progress thay vì local_t/5
                else:
                    angle = 0
                
                # Tạo clip mới với góc xoay tương ứng
                rotated = VideoClip(lambda t: img.get_frame(0), duration=0.1)
                if angle != 0:
                    import moviepy.video.fx as vfx
                    rotated = vfx.Rotate(angle=angle, unit='deg', expand=True, resample='bicubic', bg_color=None).apply(rotated)
                return rotated.get_frame(0)
            
            def create_position(t):
                local_t = t - start_time
                if t < start_time:  # Chưa đến lượt
                    return (total_width, 0)
                elif local_t < 5:  # Di chuyển trong 5 giây
                    # Tính toán vị trí cuối cùng dựa trên index
                    final_x = index * image_width
                    progress = ease_out(local_t)
                    # Di chuyển từ phải sang trái đến vị trí cuối với easing
                    current_x = total_width - (total_width - final_x) * progress
                    return (current_x, 0)
                else:  # Đã vào vị trí
                    return (index * image_width, 0)
            
            # Tạo clip với hiệu ứng
            clip = VideoClip(make_frame, duration=final_duration)
            clip = clip.with_position(create_position)
            return clip
        
        # Tạo các clips
        clips = []
        for i, (img_path, text) in enumerate(self.media_items):
            clip = create_clip(img_path, i, i * image_duration)
            clips.append(clip)
        
        # Tạo video cuối cùng với nền trong suốt
        final_bg = ColorClip(size=(total_width, screen_height), color=(0,0,0,0)).with_duration(final_duration)
        final_clip = CompositeVideoClip([final_bg] + clips, size=(total_width, screen_height), bg_color=None)
        
        # Thêm nhạc nền nếu có
        if self.background_music:
            self.progress.emit("Đang thêm nhạc nền...")
            audio = AudioFileClip(self.background_music)
            if audio.duration < final_clip.duration:
                audio = audio.loop(duration=final_clip.duration)
            else:
                audio = audio.subclipped(0, final_clip.duration)
            final_clip = final_clip.with_audio(audio)
        
        # Xuất video
        self.progress.emit("Đang xuất video...")
        final_clip.write_videofile(
            self.save_path,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=8,
            bitrate="500k",
            ffmpeg_params=["-pix_fmt", "yuv420p", "-crf", "40"]
        )
        
        # Dọn dẹp
        final_clip.close()
        if self.background_music and "audio" in locals():
            audio.close()
        
        self.finished.emit(True, "Tạo video thành công!")
