/*
  Warnings:

  - Added the required column `type` to the `Question` table without a default value. This is not possible if the table is not empty.

*/
-- CreateEnum
CREATE TYPE "QuestionType" AS ENUM ('MULTIPLE_CHOICE', 'TEXT_INPUT', 'RATING', 'FILE_UPLOAD', 'DATE_PICKER');

-- AlterTable
ALTER TABLE "Option" ADD COLUMN     "image" TEXT;

-- AlterTable
ALTER TABLE "Question" ADD COLUMN     "image" TEXT,
ADD COLUMN     "type" "QuestionType" NOT NULL;
