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
        total_width = 300
        screen_height = 100
        image_duration = 5
        image_width = 50
        target_x = 10 - image_width  # Vị trí x mục tiêu để cạnh phải của hình = 10
        # Tính toán lại thời lượng video dựa trên thời điểm hình thứ 5 về vị trí target_x
        distance_to_move = (4 * image_width + image_width) - target_x  # Khoảng cách từ vị trí bắt đầu đến target_x
        movement_time = (distance_to_move / image_width) * image_duration
        final_duration = (5 * image_duration) + movement_time
        
        def ease_out(t):
            t = t / 5  # Giữ nguyên vì đã phù hợp với 5s
            return 1 - pow(1 - t, 3)
        
        def create_clip(img_path, index, start_time):
            # Tạo animation cho hình ảnh với nền trong suốt
            img = ImageClip(img_path)
            # Chỉ resize các hình từ 1-4
            if index < 4:
                img = img.resized(width=image_width, height=screen_height)
            else:
                img = img.resized(height=screen_height)
            def make_frame(t):
                # Tính góc xoay (chỉ cho 4 ảnh đầu tiên)
                local_t = t - start_time
                if index < 4:  # Chỉ xoay 4 ảnh đầu
                    if local_t < 5:  # Tăng thời gian xoay lên 5 giây
                        progress = ease_out(local_t)
                        angle = 45 * (1 - progress)
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
            
            def create_position(t):
                local_t = t - start_time
                
                if t < start_time:
                    return (total_width, 0)
                elif local_t < 5:  # Animation đầu tiên 5s
                    final_x = min(index, 4) * image_width
                    progress = ease_out(local_t)
                    current_x = total_width - (total_width - final_x) * progress
                    return (current_x, 0)
                else:
                    current_time = t
                    current_index = int(current_time // image_duration)
                    
                    if current_index < 5:  # 4 hình đầu giữ nguyên vị trí
                        return (index * image_width, 0)
                    else:
                        # Xử lý cho hình từ số 5 trở đi
                        if current_index >= 4:  # Sau khi hình thứ 4 đã xuất hiện
                            if current_index >= index:  # Đến lượt hoặc đã qua lượt hình hiện tại
                                # Vị trí ban đầu: ngay sau hình 4
                                start_x = 4 * image_width + image_width
                                # Khoảng cách giữa các hình
                                offset = (index - 5) * image_width
                                initial_x = start_x + offset
                                
                                # Thời gian từ khi hình thứ 5 xuất hiện
                                time_since_fifth = current_time - (5 * image_duration)
                                if time_since_fifth > 0:
                                    # Di chuyển sang trái với linear để chuyển động đều
                                    max_time = movement_time
                                    move_progress = min(time_since_fifth / max_time, 1)
                                    move_distance = move_progress * distance_to_move
                                    new_x = initial_x - move_distance
                                    
                                    # Chỉ kiểm tra điều kiện ra khỏi màn hình cho các hình từ số 6 trở đi
                                    if index > 4 and new_x + image_width < 0:
                                        return (total_width * 4, 0)  # Di chuyển hình ra xa khỏi khung hình
                                    
                                    # Bỏ kiểm tra x < 1 cho hình số 5
                                    if index < 4 and new_x < 1:
                                        new_x = 0
                                    return (new_x, 0)
                            else:
                                return (total_width, 0)
                        else:
                            return (total_width, 0)
            
            # Tạo clip với hiệu ứng
            clip = VideoClip(make_frame, duration=final_duration)
            clip = clip.with_position(create_position)
            return clip
        
        # Tạo các clips
        clips = []
        for i, (img_path, text) in enumerate(self.media_items):
            clip = create_clip(img_path, i, i * image_duration)
            clips.append(clip)
        
        # Tạo video cuối cùng
        final_bg = ColorClip(size=(total_width, screen_height), color=(0,0,0)).with_duration(final_duration)  # Đổi màu nền thành trắng và bỏ alpha
        final_clip = CompositeVideoClip([final_bg] + clips, size=(total_width, screen_height))  # Bỏ bg_color=None
        
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
