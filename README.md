# THEOplayer 2.69.1 presentationTimeOffset issue reproduction project

I found that THEOplayer 2.69.1 cannot play a DASH stream under certain conditions.
Here is the conditions.
1. Live manifest
2. SegmentTimeline is used
3. `presentationTimeOffset` is larger than *Earliest Presentation Time*

For example, this is NG pattern.
```
<SegmentTemplate timescale="48000" media="BBB_32k_$Time$.mp4" initialization="BBB_32k_init.mp4" presentationTimeOffset="239617">
  <SegmentTimeline>
    <S d="239616" t="239616" r="12" />
  </SegmentTimeline>
</SegmentTemplate>
```

However, if you replace `presentationTimeOffset="239617"` with `presentationTimeOffset="239616"`, no error occurs.

I asked a question if `presentationTimeOffset` can be larger than *Earliest Presentation Time* in the DASH specification on the DASH-IF slack group.

https://dashif.slack.com/archives/C11QXV7FG/p1584610010009900

It seems that players should allow `presentationTimeOffset` being larger than *Earliest Presentation Time*

<details>
<summary>My question and the response on the DASH-IF slack group</summary>

**Tomohiro Matsuzawa**<br>
Hi, I am a little bit confused about the explanation about presentationTimeOffset in the Guidelines for Implementation.
Representation@presentationTimeOffset: the presentation time offset of the Representation in the Period, i.e. it provides the media time of the Representation that is supposed to be rendered at the start of the Period. Note that typically this time is either earliest presentation time of the first segment or a value slightly larger in order to ensure synchronization of different media components. If larger, this Representation is presented with short delay with respect to the Period start.
I think presentationTimeOffset should be smaller than earliest presentation time of the first segment to present with short delay with respect to the Period start.
My English is not good, so maybe I am just misunderstood and both are same thing?

**Sander Saares**<br>
We are doing a big update to the timing model description that should help clarify matters in v5: https://dashif-documents.azurewebsites.net/Guidelines-TimingModel/master/Guidelines-TimingModel.html

With regard to the specific statement you quoted, I agree with you. I believe the statement is in error.

That being said, the referenced v5 guidelines draft on the timing model also state that the first segment must start either before or at the period start. Starting one representation after the period start is not permitted as it would leave a gap.

**Tomohiro Matsuzawa**<br>
oh, then should it be like this in v5 guidelines?
presentationTimeOffset >= earliest presentation time of the first segment

**Daniel Silhavy**<br>
@Tomohiro Matsuzawa Yes, from a players perspective:

Timestamp Offset of the MSE Sourcebuffer(TO) = Period@start - presentationTimeOffset

Position of a segment in the buffer = Earliest Presentation Time + TSO

So yes imo PTO must be >= EPT

Otherwise you have gaps in your presentation timeline

**Tomohiro Matsuzawa**<br>
Thank you for the clarification!
</details>

I reproduced this issue on following environment.
+ macOS Catalina 10.15.2
+ Chrome 80.0.3987.163
+ THEOplayer 2.69.1(No reproduction with 2.67.0)

## How to run

```sh
$ cp [your certificate] ./cert/server.crt
$ cp [your private key] ./cert/server.key
$ pip install Flask
$ python application.py
```

Play `https://[your domain]:8443/manifest.mpd` with THEOplayer 2.69.1

You will see it doesn't start playing.

Next, comment out next line on application.py

```application.py
audio_pto += 1
```

Play the same url and you will see it start playing.
