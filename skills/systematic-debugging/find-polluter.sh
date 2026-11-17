#!/usr/bin/env bash

set -e

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <file_to_check> <test_pattern>"
  echo "Example: $0 '.git' 'src/**/*.test.ts'"
  exit 1
fi

POLLUTION_CHECK="$1"
TEST_PATTERN="$2"

echo "🔍 Searching for test that creates: ${POLLUTION_CHECK}"
echo "Test pattern: ${TEST_PATTERN}"
echo ""
TEST_PATTERN="${TEST_PATTERN#./}"
TEST_FILES=$(find . \( -path "./${TEST_PATTERN}" -o -path "./${TEST_PATTERN//\*\*\//}" \) | sort -u)
if [[ -z "${TEST_FILES}" ]]; then
  TOTAL=0
else
  TOTAL=$(printf '%s\n' "${TEST_FILES}" | wc -l | tr -d ' ')
fi

echo "Found ${TOTAL} test files"
echo ""

COUNT=0
for TEST_FILE in ${TEST_FILES}; do
  COUNT=$((COUNT + 1))
  if [[ -e "${POLLUTION_CHECK}" ]]; then
    echo "⚠️  Pollution already exists before test ${COUNT}/${TOTAL}"
    echo "   Skipping: ${TEST_FILE}"
    continue
  fi

  echo "[${COUNT}/${TOTAL}] Testing: ${TEST_FILE}"
  npm test "${TEST_FILE}" > /dev/null 2>&1 || true
  if [[ -e "${POLLUTION_CHECK}" ]]; then
    echo ""
    echo "🎯 FOUND POLLUTER!"
    echo "   Test: ${TEST_FILE}"
    echo "   Created: ${POLLUTION_CHECK}"
    echo ""
    echo "Pollution details:"
    ls -la "${POLLUTION_CHECK}"
    echo ""
    echo "To investigate:"
    echo "  npm test ${TEST_FILE}    # Run just this test"
    echo "  cat ${TEST_FILE}         # Review test code"
    exit 1
  fi
done

echo ""
echo "✅ No polluter found - all tests clean!"
exit 0
