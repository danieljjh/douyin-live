# ffmpeg -i 'https://pull-l3.douyincdn.com/third/stream-115427936031211999_or4.m3u8?auth_key=1720613729-0-0-d20d132ab56af1c3f99bd32777dbe771' -bsf:a aac_adtstoasc  -vcodec copy -c copy -crf 50 ly-7-4-2-2.mp4

ffmpeg -i 'https://pull-l3.douyincdn.com/third/stream-115513763101671903_uhd.m3u8?auth_key=1721892296-0-0-2b9c557c2a7d3fca6d9ed4a4247912e3' -bsf:a aac_adtstoasc -vcodec copy -c copy -t 3600 ly-7-18-2-1.mp4

ffmpeg -i 'https://pull-hls-l26.douyincdn.com/third/stream-115642438446744038_or4.m3u8?expire=66bf470c&sign=d3869b24cddb54885e9dcdc9632b16d0' -bsf:a aac_adtstoasc -vcodec copy -c copy -t 360 ly-8-06-nt-1.mp4

ffmpeg -i  'https://pull-hs-f5.flive.douyincdn.com/third/stream-404010822899597995_or4/index.m3u8?expire=1725867989&sign=629f889658535b0fe4bb7abde8763b7e&volcSecret=629f889658535b0fe4bb7abde8763b7e&volcTime=1725867989&major_anchor_level=common'  -vn -ab 192k   ly-240902-n-1.mp3

ffmpeg -i  'https://pull-hls-l6.douyincdn.com/radio/stream-115589953609007139/index.m3u8?k=42313d2b4acc7c32&t=1723032147' -vn -ab 192k   ly-7-31-n-1.mp3