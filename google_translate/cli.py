"""CLI for google-translate. Run with: google-translate [command] [args]"""

import argparse
import sys

from .text import translate_text
from .image import translate_image
from .docs import translate_document
from .websites import translate_website
from .voice import translate_voice


def main():
    parser = argparse.ArgumentParser(
        prog="google-translate",
        description="Translate text, images, documents, and websites via Google Translate",
    )
    parser.add_argument("--mode", choices=["browser", "direct"], default="browser",
                        help="'browser' (default, needs Chrome) or 'direct' (HTTP only, text only)")
    parser.add_argument("--headless", default=True, action=argparse.BooleanOptionalAction,
                        help="Run Chrome hidden (default: --headless)")

    sub = parser.add_subparsers(dest="command", required=True)

    # text
    tp = sub.add_parser("text", help="Translate text")
    tp.add_argument("text", help="Text to translate")
    tp.add_argument("source", nargs="?", default="auto", help="Source language (default: auto)")
    tp.add_argument("target", default="es", nargs="?", help="Target language (default: es)")

    # image
    ip = sub.add_parser("image", help="Translate image")
    ip.add_argument("path", help="Path to image file")
    ip.add_argument("source", nargs="?", default="auto")
    ip.add_argument("target", default="es", nargs="?")
    ip.add_argument("-o", "--output", default=None, help="Output file path")

    # doc
    dp = sub.add_parser("document", help="Translate document")
    dp.add_argument("path", help="Path to document file")
    dp.add_argument("source", nargs="?", default="auto")
    dp.add_argument("target", default="es", nargs="?")
    dp.add_argument("-o", "--output", default=None, help="Output file path")

    # website
    wp = sub.add_parser("website", help="Translate website")
    wp.add_argument("url", help="Website URL")
    wp.add_argument("source", nargs="?", default="auto")
    wp.add_argument("target", default="es", nargs="?")

    # voice
    vp = sub.add_parser("voice", help="Convert text to speech")
    vp.add_argument("text", help="Text to speak")
    vp.add_argument("source", nargs="?", default="en")
    vp.add_argument("target", default="am", nargs="?")
    vp.add_argument("-o", "--output", default="output.mp3", help="Output audio file (default: output.mp3)")

    args = parser.parse_args()

    if args.command == "text":
        r = translate_text(args.text, args.source, args.target,
                          mode=args.mode, headless=args.headless)
        if "error" in r:
            print(f"Error: {r['error']}", file=sys.stderr)
            sys.exit(1)
        print(r["translated"])

    elif args.command == "image":
        r = translate_image(args.path, args.source, args.target,
                           mode=args.mode, headless=args.headless)
        if not r.get("success"):
            print(f"Error: {r.get('error', 'Unknown')}", file=sys.stderr)
            sys.exit(1)
        out = args.output or f"translated_{args.path}"
        with open(out, "wb") as f:
            f.write(r["image_data"])
        print(f"Saved {r['translated_size']} bytes to {out}")

    elif args.command == "document":
        r = translate_document(args.path, args.source, args.target,
                              mode=args.mode, headless=args.headless)
        if not r.get("success"):
            print(f"Error: {r.get('error', 'Unknown')}", file=sys.stderr)
            sys.exit(1)
        if r.get("document_data"):
            out = args.output or f"translated_{args.path}"
            with open(out, "wb") as f:
                f.write(r["document_data"])
            print(f"Saved {r['size']} bytes to {out}")
        elif r.get("document_text"):
            out = args.output or f"translated_{args.path}.txt"
            with open(out, "w", encoding="utf-8") as f:
                f.write(r["document_text"])
            print(f"Saved text to {out}")

    elif args.command == "website":
        r = translate_website(args.url, args.source, args.target,
                             mode=args.mode, headless=args.headless)
        if not r.get("success"):
            print(f"Error: {r.get('error', 'Unknown')}", file=sys.stderr)
            sys.exit(1)
        print(f"Title: {r['title']}")
        print(f"URL: {r['url']}")

    elif args.command == "voice":
        r = translate_voice(args.text, args.source, args.target)
        if not r.get("audio_data"):
            print("Error: No audio data", file=sys.stderr)
            sys.exit(1)
        with open(args.output, "wb") as f:
            f.write(r["audio_data"])
        print(f"Audio saved to {args.output}")


if __name__ == "__main__":
    main()
