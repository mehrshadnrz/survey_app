-- AlterEnum
-- This migration adds more than one value to an enum.
-- With PostgreSQL versions 11 and earlier, this is not possible
-- in a single migration. This can be worked around by creating
-- multiple migrations, each migration adding only one value to
-- the enum.


ALTER TYPE "QuestionType" ADD VALUE 'OPENING';
ALTER TYPE "QuestionType" ADD VALUE 'ENDING';

-- AlterTable
ALTER TABLE "Answer" ADD COLUMN     "creationDate" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "score" DOUBLE PRECISION;

-- AlterTable
ALTER TABLE "Response" ADD COLUMN     "startTime" TIMESTAMP(3),
ADD COLUMN     "totalScore" DOUBLE PRECISION;

-- CreateTable
CREATE TABLE "FactorValue" (
    "id" SERIAL NOT NULL,
    "factorId" INTEGER NOT NULL,
    "responseId" INTEGER NOT NULL,
    "value" INTEGER NOT NULL,

    CONSTRAINT "FactorValue_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "FactorValue" ADD CONSTRAINT "FactorValue_factorId_fkey" FOREIGN KEY ("factorId") REFERENCES "Factor"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "FactorValue" ADD CONSTRAINT "FactorValue_responseId_fkey" FOREIGN KEY ("responseId") REFERENCES "Response"("id") ON DELETE CASCADE ON UPDATE CASCADE;
