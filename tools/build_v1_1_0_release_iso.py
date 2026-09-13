#!/usr/bin/env python3
"""Build and statically verify the Disc 1 v1.1.0 release ISO.

The pinned v1.0.0 release is the immutable parent.  This build makes exactly
two approved payload changes:

* restore the Square-button glyph in the field search tutorial by repairing
  two wrongly double-based logical glyph codes in DATA/00061000.MDZ;
* replace MOVIE/GRM10.MOV with the full 17-cue resynchronised hard-sub movie.

The clean Disc 1 image is pinned as the eventual full-xdelta source, but is
not used as a mutable build parent here.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from build_external_subtitle_container_test import iso_entry
from scan_scenario_resources import IsoImage


ROOT = Path(__file__).resolve().parents[1]
BUILD_ROOT = ROOT / "build/v1.1.0-release-20260914"
CLEAN_ISO = Path(
    "/Users/j.swon/Desktop/Grandia3_KR/Original ISO/"
    "Grandia III (Japan) (Disc 1).iso"
)
CLEAN_SIZE = 4_598_890_496
CLEAN_SHA256 = "c588a7dada3bf7175bfe97b238b0ab4c77df6401a58d766829aec9d92f3596e8"
PARENT_ISO = (
    ROOT / "build/v1.0.0-release-20260907/Grandia3_KR_Disc1_v1.0.0.iso"
)
PARENT_SIZE = 4_598_890_496
PARENT_SHA256 = "561630a8f914685e0c24f749f20f3773594bd5fbd2d54218a0bdf86cdcccef55"

TUTORIAL_ENTRY = "DATA/00061000.MDZ"
TUTORIAL_EXTENT = 1_916_785
TUTORIAL_SIZE = 2_976_837
TUTORIAL_SHA256 = "badf0be743b37e1151bde6cff43700eb61bb1f6c7ac823ed7ec912a975a412e3"
TUTORIAL_MDT_PATCHES = {
    0x00448994: (bytes.fromhex("D8 F9"), bytes.fromhex("B8 F9")),
    0x004489B0: (bytes.fromhex("D8 F9"), bytes.fromhex("B8 F9")),
}

GRM10_ENTRY = "MOVIE/GRM10.MOV"
GRM10_EXTENT = 548_511
GRM10_SIZE = 99_680_256
GRM10_PARENT_SHA256 = "ba44defed3ff67feea9fd3acb50693f434541720022789f026e2fb018dbc455d"
GRM10_CANDIDATE = Path(
    "/Users/j.swon/Desktop/Grandia3_KR/build/"
    "grm10-hardsub-full-resync-20260914/GRM10_hardsub_referenceclock_candidate.MOV"
)
GRM10_CANDIDATE_SHA256 = "171ea2babe098350847e612191c8aa1638a4f54a73f27ddd46e9d75958c850c7"
GRM10_SRT = Path("/Users/j.swon/Desktop/Grandia3_KR/MOVIE/GRM10.srt")
GRM10_SRT_SHA256 = "2b0c12a4ecd1c23dd4b5c665fde102b90880d88024d6f501d887d9caf64e0c35"
GRM10_REPORT = Path(
    "/Users/j.swon/Desktop/Grandia3_KR/build/grm10-full-audit-20260914/"
    "GRM10_FULL_RESYNC_REPORT.json"
)
GRM10_REPORT_SHA256 = "51d821568a89bcd1f5eb700980c6c5f3072473e7d9b4faa51eae794d35be2af0"

GRANDIA_TOOL = ROOT / "tools/grandia3-tool-active/target/release/grandia3-tool"
OUTPUT_ISO = BUILD_ROOT / "Grandia3_KR_Disc1_v1.1.0.iso"
PLAN = BUILD_ROOT / "replacement-plan.json"
ISO_REPORT = BUILD_ROOT / "v1.1.0-ISO-BUILD-REPORT.json"
STATIC_REPORT = BUILD_ROOT / "v1.1.0-STATIC-AND-ISO-VERIFICATION.json"
RUNTIME_RESULT = BUILD_ROOT / "v1.1.0-RUNTIME-RESULT.json"

CRITICAL_INHERITED = (
    "GR3SUB.BIN",
    "SLPM_659.76",
    "FIELD.BIN",
    "FLIGHT.BIN",
    "BATTLE.BIN",
    "SYS/GR3.MDZ",
    "DATA/00150100.MDZ",
    "DATA/00151200.MDZ",
    "DATA/00180800.MDZ",
    "DATA/00270100.MDZ",
    "DATA/00397700.MDZ",
    "DATA/01080505.MDZ",
    "DATA/01120102.MDZ",
    "DATA/30000000.MDZ",
    "MOVIE/GRM16.MOV",
    "MOVIE/GRM17.MOV",
    "MOVIE/GRM18.MOV",
    "MOVIE/GRM20.MOV",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(16 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def run(command: list[str]) -> str:
    result = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"command failed ({result.returncode}): {' '.join(command)}\n{result.stdout}"
        )
    return result.stdout


def population(path: Path) -> dict[str, object]:
    with IsoImage(path) as image:
        return {item.path.upper(): item for item in image.entries() if not item.is_dir}


def validate_grm10() -> dict[str, object]:
    pinned = {
        GRM10_CANDIDATE: (GRM10_SIZE, GRM10_CANDIDATE_SHA256),
        GRM10_SRT: (None, GRM10_SRT_SHA256),
        GRM10_REPORT: (None, GRM10_REPORT_SHA256),
    }
    for path, (expected_size, expected_hash) in pinned.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        if expected_size is not None and path.stat().st_size != expected_size:
            raise ValueError(f"pinned GRM10 size changed: {path}")
        if sha256_file(path) != expected_hash:
            raise ValueError(f"pinned GRM10 hash changed: {path}")
    report = json.loads(GRM10_REPORT.read_text(encoding="utf-8"))
    candidate = report["candidate"]
    if (
        report.get("status") != "candidate_ready_for_pcsx2_playback_verification"
        or report["subtitle_audit"]["cue_count"] != 17
        or report["subtitle_audit"]["source_srt_sha256"] != GRM10_SRT_SHA256
        or candidate["sha256"] != GRM10_CANDIDATE_SHA256
        or int(candidate["size"]) != GRM10_SIZE
        or not candidate["header_preserved"]
        or not candidate["audio_sectors_preserved_byte_exact"]
        or int(candidate["audio_sector_count"]) != 3301
        or candidate["audio_sha256"]
        != "b8fec6c8f5fc8d6e6b3182890abfb8143f98d69c7174df05bc81e1d86febe7c1"
        or candidate["mpeg2_ps_decode"] != "PASS"
        or int(candidate["pack_count"]) != 5671
        or int(candidate["non_0x4000_pack_gaps"]) != 0
        or int(candidate["scr_decreases"]) != 0
        or int(candidate["negative_pts_minus_scr"]) != 0
        or int(candidate["negative_dts_minus_scr"]) != 0
    ):
        raise ValueError("GRM10 component report invariants changed")
    return report


def build_tutorial_candidate(parent_payload: bytes) -> tuple[Path, dict[str, object]]:
    source_dir = BUILD_ROOT / "source"
    candidate_dir = BUILD_ROOT / "candidate"
    source_dir.mkdir(parents=True, exist_ok=True)
    candidate_dir.mkdir(parents=True, exist_ok=True)
    source_mdz = source_dir / "00061000.MDZ"
    source_mdt = source_dir / "00061000.MDT"
    candidate_mdt = candidate_dir / "00061000.MDT"
    candidate_mdz = candidate_dir / "00061000.MDZ"
    source_mdz.write_bytes(parent_payload)
    run([str(GRANDIA_TOOL), "decode-mdz", str(source_mdz), "--output", str(source_mdt)])

    source = source_mdt.read_bytes()
    output = bytearray(source)
    changed_offsets: list[int] = []
    patch_rows: list[dict[str, object]] = []
    for offset, (expected, replacement) in TUTORIAL_MDT_PATCHES.items():
        current = source[offset:offset + len(expected)]
        if current != expected:
            raise ValueError(
                f"tutorial source mismatch at 0x{offset:X}: {current.hex()}"
            )
        output[offset:offset + len(expected)] = replacement
        patch_rows.append(
            {
                "offset": f"0x{offset:X}",
                "original_hex": expected.hex(" ").upper(),
                "replacement_hex": replacement.hex(" ").upper(),
                "meaning": "double-based <G08B8> repaired to logical Square-button code",
            }
        )
    candidate = bytes(output)
    if len(candidate) != len(source):
        raise ValueError("tutorial decoded MDT size changed")
    changed_offsets = [
        index for index, (before, after) in enumerate(zip(source, candidate))
        if before != after
    ]
    expected_changed = sorted(TUTORIAL_MDT_PATCHES)
    if changed_offsets != expected_changed:
        raise ValueError(
            f"unexpected decoded tutorial changes: {[hex(x) for x in changed_offsets]}"
        )
    candidate_mdt.write_bytes(candidate)

    with tempfile.TemporaryDirectory(prefix="gr3-v110-tutorial-") as temp_name:
        pack_dir = Path(temp_name) / "packed"
        run(
            [
                str(GRANDIA_TOOL),
                "build-mdz-candidate",
                str(candidate_mdt),
                "--header-template",
                str(source_mdz),
                "--output-dir",
                str(pack_dir),
                "--relocatable",
            ]
        )
        packed = list(pack_dir.glob("*.MDZ"))
        if len(packed) != 1:
            raise ValueError("unexpected DATA/00061000 MDZ encoder output")
        shutil.copyfile(packed[0], candidate_mdz)
        reverse_mdt = Path(temp_name) / "00061000.reverse.MDT"
        run(
            [
                str(GRANDIA_TOOL),
                "decode-mdz",
                str(candidate_mdz),
                "--output",
                str(reverse_mdt),
            ]
        )
        if reverse_mdt.read_bytes() != candidate:
            raise ValueError("tutorial candidate MDZ reverse decode mismatch")

    parent_sectors = (TUTORIAL_SIZE + 2047) // 2048
    candidate_sectors = (candidate_mdz.stat().st_size + 2047) // 2048
    if candidate_sectors > parent_sectors:
        raise ValueError("tutorial candidate exceeds original sector allocation")
    return candidate_mdz, {
        "entry": TUTORIAL_ENTRY,
        "extent": TUTORIAL_EXTENT,
        "parent_mdz_size": TUTORIAL_SIZE,
        "parent_mdz_sha256": TUTORIAL_SHA256,
        "source_mdt_size": len(source),
        "source_mdt_sha256": sha256_bytes(source),
        "candidate_mdt_size": len(candidate),
        "candidate_mdt_sha256": sha256_bytes(candidate),
        "candidate_mdz_size": candidate_mdz.stat().st_size,
        "candidate_mdz_sha256": sha256_file(candidate_mdz),
        "parent_sectors": parent_sectors,
        "candidate_sectors": candidate_sectors,
        "changed_byte_count": len(changed_offsets),
        "changed_offsets": [f"0x{offset:X}" for offset in changed_offsets],
        "patches": patch_rows,
    }


def verify_population(output_iso: Path, tutorial_candidate_size: int) -> dict[str, object]:
    parent = population(PARENT_ISO)
    output = population(output_iso)
    if set(parent) != set(output):
        raise ValueError("ISO path population changed")
    metadata_changes: dict[str, dict[str, object]] = {}
    for path in parent:
        before = parent[path]
        after = output[path]
        if before.extent != after.extent:
            raise ValueError(f"ISO entry extent changed: {path}")
        if before.size != after.size:
            metadata_changes[path] = {"before": before.size, "after": after.size}
    expected = {}
    if tutorial_candidate_size != TUTORIAL_SIZE:
        expected[TUTORIAL_ENTRY] = {
            "before": TUTORIAL_SIZE,
            "after": tutorial_candidate_size,
        }
    if metadata_changes != expected:
        raise ValueError(f"unexpected entry-size changes: {metadata_changes}")
    if (output[GRM10_ENTRY].extent, output[GRM10_ENTRY].size) != (
        GRM10_EXTENT,
        GRM10_SIZE,
    ):
        raise ValueError("GRM10 extent or size changed")
    return {
        "file_count": len(output),
        "path_population_preserved": True,
        "all_extents_preserved": True,
        "entry_size_changes": metadata_changes,
    }


def verify_inherited(output_iso: Path) -> dict[str, object]:
    rows: dict[str, object] = {}
    for entry in CRITICAL_INHERITED:
        before_extent, before_size, before = iso_entry(PARENT_ISO, entry)
        after_extent, after_size, after = iso_entry(output_iso, entry)
        if (before_extent, before_size, before) != (after_extent, after_size, after):
            raise ValueError(f"critical inherited entry changed: {entry}")
        rows[entry] = {
            "extent": after_extent,
            "size": after_size,
            "sha256": sha256_bytes(after),
            "byte_exact_v1_0_0": True,
        }
    if rows["SYS/GR3.MDZ"]["sha256"] != (
        "b326bfa6bb93058f5eff45a25fe7b96f976a5ad292d352af758e4ee59e43ced8"
    ):
        raise ValueError("SYS/GR3.MDZ font payload changed")
    return rows


def verify_reverse_7z(output_iso: Path, entry: str, expected: bytes) -> None:
    result = subprocess.run(
        ["7z", "x", "-so", str(output_iso), entry],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode or result.stdout != expected:
        raise ValueError(f"independent 7-Zip reverse failed: {entry}")


def main() -> int:
    for path, size, digest, label in (
        (CLEAN_ISO, CLEAN_SIZE, CLEAN_SHA256, "CLEAN Disc 1"),
        (PARENT_ISO, PARENT_SIZE, PARENT_SHA256, "v1.0.0 parent"),
    ):
        if not path.is_file() or path.stat().st_size != size or sha256_file(path) != digest:
            raise ValueError(f"pinned {label} ISO changed")
    if not GRANDIA_TOOL.is_file():
        raise FileNotFoundError(GRANDIA_TOOL)
    grm10_report = validate_grm10()

    tutorial_extent, tutorial_size, tutorial_payload = iso_entry(
        PARENT_ISO, TUTORIAL_ENTRY
    )
    if (
        (tutorial_extent, tutorial_size) != (TUTORIAL_EXTENT, TUTORIAL_SIZE)
        or sha256_bytes(tutorial_payload) != TUTORIAL_SHA256
    ):
        raise ValueError("pinned v1.0.0 tutorial entry changed")
    grm_extent, grm_size, grm_payload = iso_entry(PARENT_ISO, GRM10_ENTRY)
    if (
        (grm_extent, grm_size) != (GRM10_EXTENT, GRM10_SIZE)
        or sha256_bytes(grm_payload) != GRM10_PARENT_SHA256
    ):
        raise ValueError("pinned v1.0.0 GRM10 entry changed")

    BUILD_ROOT.mkdir(parents=True, exist_ok=True)
    tutorial_candidate, tutorial_report = build_tutorial_candidate(tutorial_payload)
    plan = {
        "schema_version": 1,
        "build": "GRANDIA3-KR-DISC1-v1.1.0",
        "parent_iso": str(PARENT_ISO.resolve()),
        "parent_iso_sha256": PARENT_SHA256,
        "scope": "v1.0.0 plus Square tutorial glyph repair and GRM10 full resync",
        "replacements": [
            {
                "entry": TUTORIAL_ENTRY,
                "replacement": str(tutorial_candidate.resolve()),
                "size": tutorial_candidate.stat().st_size,
                "sha256": sha256_file(tutorial_candidate),
                "purpose": "restore two Square-button glyph codes without changing font data",
            },
            {
                "entry": GRM10_ENTRY,
                "replacement": str(GRM10_CANDIDATE.resolve()),
                "size": GRM10_SIZE,
                "sha256": GRM10_CANDIDATE_SHA256,
                "purpose": "replace pre-resync hard subtitles with the full 17-cue resync",
            },
        ],
    }
    PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_ISO.unlink(missing_ok=True)
    run(
        [
            "python3",
            str(ROOT / "tools/build_integrated_test_iso.py"),
            str(PARENT_ISO),
            str(PLAN),
            str(OUTPUT_ISO),
            "--report",
            str(ISO_REPORT),
        ]
    )
    iso_report = json.loads(ISO_REPORT.read_text(encoding="utf-8"))
    if (
        iso_report["source_sha256"] != PARENT_SHA256
        or int(iso_report["source_size"]) != PARENT_SIZE
        or int(iso_report["output_size"]) != PARENT_SIZE
        or int(iso_report["replacement_count"]) != 2
        or int(iso_report["relocated_count"]) != 0
        or iso_report["extend_tail"]
        or not iso_report["reverse_verified"]
        or not iso_report["udf_reverse_verified"]
    ):
        raise ValueError("v1.1.0 ISO writer verification failed")
    output_hash = sha256_file(OUTPUT_ISO)
    if output_hash != iso_report["output_sha256"]:
        raise ValueError("v1.1.0 ISO hash/report mismatch")

    with tempfile.TemporaryDirectory(prefix="gr3-v110-repeat-") as temp_name:
        repeat_iso = Path(temp_name) / OUTPUT_ISO.name
        repeat_report = Path(temp_name) / "repeat-report.json"
        run(
            [
                "python3",
                str(ROOT / "tools/build_integrated_test_iso.py"),
                str(PARENT_ISO),
                str(PLAN),
                str(repeat_iso),
                "--report",
                str(repeat_report),
            ]
        )
        if sha256_file(repeat_iso) != output_hash:
            raise ValueError("two independent v1.1.0 ISO builds differ")

    tutorial_result = iso_entry(OUTPUT_ISO, TUTORIAL_ENTRY)
    grm_result = iso_entry(OUTPUT_ISO, GRM10_ENTRY)
    tutorial_expected = tutorial_candidate.read_bytes()
    grm_expected = GRM10_CANDIDATE.read_bytes()
    if tutorial_result != (
        TUTORIAL_EXTENT,
        len(tutorial_expected),
        tutorial_expected,
    ):
        raise ValueError("v1.1.0 tutorial reverse extraction differs")
    if grm_result != (GRM10_EXTENT, GRM10_SIZE, grm_expected):
        raise ValueError("v1.1.0 GRM10 reverse extraction differs")
    verify_reverse_7z(OUTPUT_ISO, TUTORIAL_ENTRY, tutorial_expected)
    verify_reverse_7z(OUTPUT_ISO, GRM10_ENTRY, grm_expected)

    image_population = verify_population(OUTPUT_ISO, len(tutorial_expected))
    inherited = verify_inherited(OUTPUT_ISO)
    report = {
        "schema_version": 1,
        "version": "1.1.0",
        "build": "GRANDIA3-KR-DISC1-v1.1.0",
        "status": "STATIC_AND_ISO_REVERSE_PASS_RUNTIME_PENDING",
        "clean_xdelta_source": {
            "iso": str(CLEAN_ISO.resolve()),
            "size": CLEAN_SIZE,
            "sha256": CLEAN_SHA256,
        },
        "parent": {
            "build": "GRANDIA3-KR-DISC1-v1.0.0",
            "iso": str(PARENT_ISO.resolve()),
            "size": PARENT_SIZE,
            "sha256": PARENT_SHA256,
        },
        "changes": {
            "search_tutorial_square_button": tutorial_report,
            "grm10_full_resync": {
                "entry": GRM10_ENTRY,
                "extent": GRM10_EXTENT,
                "size": GRM10_SIZE,
                "parent_sha256": GRM10_PARENT_SHA256,
                "candidate_sha256": GRM10_CANDIDATE_SHA256,
                "cue_count": 17,
                "header_preserved": True,
                "original_audio_sector_count": 3301,
                "original_audio_sha256": grm10_report["candidate"]["audio_sha256"],
                "runtime_status": "PENDING_USER_PLAYBACK",
            },
        },
        "checks": {
            "pinned_clean_and_v1_0_0_parent": "PASS",
            "exact_two_entry_allowlist": "PASS",
            "tutorial_exact_two_bytes_only": "PASS",
            "tutorial_mdz_reverse_decode_exact": "PASS",
            "grm10_component_hash_and_stream_metrics": "PASS",
            "same_iso_size_and_all_entry_extents": "PASS",
            "no_tail_extension_or_relocation": "PASS",
            "iso_double_build_byte_identical": "PASS",
            "iso9660_and_udf_reverse_verified": "PASS",
            "independent_7zip_reverse_both_entries": "PASS",
            "sys_gr3_font_and_ten_slot_inherited_exact": "PASS",
            "critical_v1_0_0_entries_inherited_exact": "PASS",
        },
        "iso_population": image_population,
        "critical_inherited_entries": inherited,
        "result": {
            "iso": str(OUTPUT_ISO.resolve()),
            "size": OUTPUT_ISO.stat().st_size,
            "sha256": output_hash,
            "replacement_plan": str(PLAN.resolve()),
            "iso_build_report": str(ISO_REPORT.resolve()),
        },
        "runtime_checklist": [
            "PCSX2를 완전히 종료하고 v1.1.0 ISO로 cold boot",
            "필드 이동 튜토리얼에서 검색 버튼이 □ 아이콘으로 표시되는지 확인",
            "해당 튜토리얼 종료 뒤 필드 조작이 가능한지 확인",
            "GRM10의 17개 자막이 음성에 맞게 표시되는지 처음부터 끝까지 확인",
            "GRM10 음성·영상 종료 뒤 다음 장면으로 정상 전환되는지 확인",
        ],
    }
    STATIC_REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    RUNTIME_RESULT.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "version": "1.1.0",
                "status": "RUNTIME_PENDING_USER_TEST",
                "iso_sha256": output_hash,
                "results": {},
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUTPUT_ISO.resolve())
    print(output_hash)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
