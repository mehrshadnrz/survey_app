/*
  Warnings:

  - Added the required column `timerOnQuestion` to the `ExamSession` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "ExamSession" ADD COLUMN     "timerOnQuestion" BOOLEAN NOT NULL;
