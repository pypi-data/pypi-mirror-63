#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from captcha.image import ImageCaptcha
from captcha.audio import AudioCaptcha


def gen_image(string, outfile, font=None):

    image_outfile_name = outfile + ".png"

    image = ImageCaptcha(fonts=font)
    image.write(string, image_outfile_name)


def gen_audio(string, outfile, voicedir=None):

    audio_outfile_name = outfile + ".wav"

    audio = AudioCaptcha(voicedir=voicedir)
    audio.write(string, audio_outfile_name)


def main():

    import argparse

    parser = argparse.ArgumentParser(prog="pycaptchagen")

    parser.add_argument(
        "string",
        help=(
            "The string of characters you want garbled into a \"CAPTCHA\". "
            "If it contains any spaces or special characters, it should be enclosed in quotation marks."
        )
    )
    parser.add_argument(
        "outfile",
        help=(
            "File name to which the \"CAPTCHA\" should be written. "
            "Do not include file extension, which is added automatically (.png for image, .wav for audio)."
        )
    )
    parser.add_argument(
        "--audio",
        action="store_true",
        help=(
            "Also generate an audio file for use by visually impaired users. "
            "Format will be WAV. Will be saved with same filename as image, but with automatic .wav file extension."
        )
    )
    parser.add_argument(
        "--noimage",
        action="store_true",
        help=(
            "Do not generate image file. Use only with --audio if you want only the audio file, with no image."
        )
    )
    parser.add_argument(
        "--font",
        action="append",
        help=(
            "Optionally specify your own font to use for the image. "
            "Can be used multiple times to specify multiple fonts for the image generator to choose from."
        )
    )
    parser.add_argument(
        "--voicedir",
        help=(
            "Optionally specify a directory containing your own voice files for generating audio. "
            "See Python captcha module for the required format for the voice files."
        )
    )

    args = parser.parse_args()

    if not args.noimage:
        gen_image(args.string, args.outfile, args.font)

    if args.audio:
        gen_audio(args.string, args.outfile, args.voicedir)
